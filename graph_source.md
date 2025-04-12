---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	reservation_agent(reservation_agent)
	data_extractor(data_extractor)
	router(router)
	fetch_reservations_tool(fetch_reservations_tool)
	add_reservation_tool(add_reservation_tool)
	update_reservation_tool(update_reservation_tool)
	delete_reservation_tool(delete_reservation_tool)
	check_availability_tool(check_availability_tool)
	end(end)
	__end__([<p>__end__</p>]):::last
	__start__ --> reservation_agent;
	add_reservation_tool --> end;
	check_availability_tool --> reservation_agent;
	data_extractor --> router;
	delete_reservation_tool --> reservation_agent;
	end --> __end__;
	fetch_reservations_tool --> end;
	update_reservation_tool --> reservation_agent;
	reservation_agent -.-> data_extractor;
	reservation_agent -.-> end;
	router -.-> fetch_reservations_tool;
	router -.-> add_reservation_tool;
	router -.-> update_reservation_tool;
	router -.-> delete_reservation_tool;
	router -.-> check_availability_tool;
	router -.-> end;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
