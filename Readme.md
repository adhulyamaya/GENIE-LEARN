
1)/recommend_courses/<user_id>/



2)Django receives the request and runs the recommend_courses view:

    *It fetches the User by user_id

    *Extracts the user's skills

    *Fetches all published Course entries

    *Builds a prompt using those skills and courses

    *Sends the prompt to GrouQ API using      call_grouq_api()

    *Returns the LLM's raw course recommendations as a JSON response