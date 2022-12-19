Annotates entries' textual descriptions via DBpedia Spotlight API. 
Tailored to that specific purpose and is not intended for usage outside the container,
as no meaningful abstraction or extensive configuration options are provided. 

Requires the following environment variables to be set:
<pre>
MONGO_URI
</pre>
Optionally, also consider setting `CALLS_PER_SECOND`, to rate limit API calls. Default is 2.

Build (in directory) with
`docker build .`
