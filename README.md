# NaturalInteligenceHomeExercize

## solution explained
this is a very simplified class designed to contain its data in memory and called periodically by it's customer

- the class checks whether last score update time was before previous 5 AM, and yes, it recalculates words semantics, else, returns current words score
- the return ds is a list of (word, word_score) tuple ordered as requested, as it is believed the score is important, and not just the order

## possible improvements

- the communication api, as I wrote all top down and haven't got to it.
things to consider in communication util:
    - server can be busy, communication should have a retry in case 5xx server error is returned, within retries limit and a short sleep between tries
- for being more testable and modular:
    - each endpoint should have its own module and provided to analytic module constructor 
    - each endpoint module should use a comutil module to handle communication to server
    - these changes would allow easy improvements to end point clients and will allow testability as each module can be easily mocked
    - the words score should be cached by the ds endpoint client and not in analytic module
- for being more scalable and robust:
    - persistence layer (db) will decouple analytic process resources and results, as they can be retained adn regained even if the process restarted, and will not have a toll on process RAM, and can scale up/down id needed
    
## bugs
- there is an implementation bug on the time window check
- there is also a logical bug on the time window check regardless of its implementation as its only the DS layer that is being updated daily at 5AM, the ads can change in higher frequency and current design will miss such changes not return accurate words score
 
