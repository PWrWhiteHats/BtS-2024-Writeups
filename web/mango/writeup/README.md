# Writeup

### 1. Overview

Visit `api-docs`. The `_id` attribute and challenge name suggest that MongoDB is used. We can POST a new fruit, which does nothing and we can GET fruit given its `id`.

### 2. Solution

Note the GET URL. Perform an NoSQL injection, e.g.,
```
http://URL:PORT/fruits?id[$ne]=661c4cf05717c55d8ceb5d23
```

which should return all fruits, which `id` does not equal `661c4cf05717c55d8ceb5d23`, including the flag.