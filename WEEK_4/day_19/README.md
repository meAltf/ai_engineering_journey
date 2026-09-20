# Terms:
    - tool: normal python function(calculator, web_search)
    - Tool node: Wrappper that calls those tools using state

# old flow:
    loop:
    plan_step()
        if final → return
        else → execute_tool()

# lang graph flow:
    planner_node → (decision)
            → tool_node → planner_node
            → END
