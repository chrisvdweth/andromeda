from andromeda.app.closeup import QueryProcessor


query_processor = QueryProcessor()

q = 'vivocity monday evening'

print query_processor.process(q)
