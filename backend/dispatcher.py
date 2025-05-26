from roles import pm, sw_engineer, web_research, sales, marketing, project_manager

ROLE_HANDLERS = {
    "pm": pm.generate_pm_output,
    "software_engineer": sw_engineer.handle,
    "web_researcher": web_research.handle,
    "sales_rep": sales.handle,
    "marketing": marketing.handle,
    "project_manager": project_manager.handle,
}

def dispatch_role(role: str, input_data: str):
    handler = ROLE_HANDLERS.get(role)
    if not handler:
        return f"Role '{role}' not supported."
    return handler(input_data)