def provide_list_query(user_id):
    return """select S.id as service_id, S.service_category as service_category, O.id as order_id, O.user_id as request_user_id, O.timestamp as order_time,  S.user_id as server_provider,
                S.timestamp as service_time, O.status as status
                from service_services  S LEFT JOIN service_order O on S.id = O.service_id
                where S.user_id = {} and (O.timestamp = 
                (SELECT Max(service_order.timestamp) 
                from service_order inner JOIN service_services on service_order.service_id = service_services.id where service_services.user_id = S.user_id
                ) or O.timestamp is NULL)""".format(
        user_id
    )
