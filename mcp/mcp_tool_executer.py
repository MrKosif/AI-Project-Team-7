import re
from mcp import ClientSession
from mcp_tool_fetcher import get_structured_tools

async def rule_checker(arg_schema: dict, value) -> str:
    """
    Tek bir property şeması (arg_schema) ve value alır.
    - type: sadece "string" desteklenir.
    - minLength, maxLength, pattern varsa sırayla kontrol eder.
    - Başarılıysa boş string ("") döner.
    - Başarısızsa açıklayıcı bir hata mesajı string'i döner.
    """
    expected_type = arg_schema.get("type", "string")
    if expected_type != "string":
        return f"unsupported type: {expected_type}"

    if not isinstance(value, str):
        return "value is not a string"

    minlen = arg_schema.get("minLength")
    if minlen is not None:
        try:
            minlen_i = int(minlen)
        except Exception:
            return "invalid minLength in schema"
        if len(value) < minlen_i:
            return f"length {len(value)} < minLength ({minlen_i})"

    maxlen = arg_schema.get("maxLength")
    if maxlen is not None:
        try:
            maxlen_i = int(maxlen)
        except Exception:
            return "invalid maxLength in schema"
        if len(value) > maxlen_i:
            return f"length {len(value)} > maxLength ({maxlen_i})"

    pattern = arg_schema.get("pattern")
    if pattern:
        try:
            prog = re.compile(pattern)
        except re.error:
            return "invalid pattern in schema"
        if not prog.fullmatch(value):
            return f"value does not match pattern: {pattern}"

    # tüm kontroller geçti
    return ""


async def arg_checker(tool_args: dict, input_schema: dict) -> tuple:
    """
    Verilen tool_args'ı input_schema ile doğrular.
    - Eksik required alanları errors'a ekler.
    - Verilen alanların her birini rule_checker ile doğrular; rule_checker'ın döndürdüğü
      hata mesajı varsa bunu errors'a ekler.
    Döner: (ok: bool, errors: list)
    """
    errors = []
    props = (input_schema or {}).get("properties", {})
    required = (input_schema or {}).get("required", [])
    args = tool_args or {}

    # required kontrolleri
    for req in required:
        if req not in args:
            errors.append({"field": req, "reason": "missing required"})

    # verilen alanların doğrulanması (rule_checker artık str döndürüyor)
    for name, schema in props.items():
        if name in args:
            msg = await rule_checker(schema, args[name])
            if msg:  # boş string => geçerli, dolu string => hata mesajı
                errors.append({"field": name, "reason": msg})

    return (len(errors) == 0, errors)


async def execute_tool_with_params(tool_name: str, tool_args: dict, session: ClientSession) -> dict:
    """
    Belirtilen araç adını ve argümanlarını kullanarak MCP aracını çalıştırır.
    Validation için arg_checker kullanır; validation hatalarında detaylı mesaj döner.
    """
    tools = await get_structured_tools(session)
    tool = next((t for t in tools if t.get("name") == tool_name), None)
    if not tool:
        return {"error": "tool_not_found", "tool": tool_name}

    schema = tool.get("input_schema", {}) or {}
    ok, errors = await arg_checker(tool_args, schema)
    if not ok:
        return {"error": "validation_error", "errors": errors}

    try:
        tool_resp = await session.call_tool(tool_name, tool_args)
    except Exception as e:
        return {"error": "execution_exception", "message": str(e)}

    if getattr(tool_resp, "error", None):
        return {"error": "execution_error", "message": str(tool_resp.error)}

    return {"ok": True, "result": tool_resp}