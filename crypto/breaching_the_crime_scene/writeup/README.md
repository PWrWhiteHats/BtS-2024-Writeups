# Breaching the Crime scene

https://breachattack.com/
https://breachattack.com/resources/BREACH%20-%20SSL,%20gone%20in%2030%20seconds.pdf
https://breachattack.com/resources/BREACH%20-%20BH%202013%20-%20PRESENTATION.pdf
https://hpc-notes.soton.ac.uk/talks/bullrun/Crime_slides.pdf

The goal of the challenge was to showcase the famous CRIME/BREACH attack on TLS. Those attacks exploit compression in order to "break" TLS and recover a secret password.

# CRIME/BREACH attack

The concept of CRIME/BREACH attack is very simple. Assume that you control some part of the plaintext, and the rest is secret. The plaintext is then compressed using `LZ77` (e.g. `gzip`, `deflate`) and then encrypted. If you can see the resulting ciphertext (e.g. when you control the network or have a packet sniffer), then you can decrypt parts of the secret plaintext.

To understand how, first see how `LZ77` works:

It scans input, looks for repeated strings and replaces them with back-references to last occurrence as (distance, length). Example:

`Google is so googley -> Google is so g(-13, 5)y`

The BREACH/CRIME attack makes use of this. Suppose we control the `user_data` param in the following query, and the `token` is a secret appended by the server, that we want to learn:

`...user_data=<data>&token=abcd`

We can then use the compression oracle in the following way. We set our input to be the prefix of the secret (`token=`) and then bruteforce every possible character at the next position. Notice what happens after compression:

* If we are wrong:
  
`...user_data=token=x&token=abcd`

`...user_data=token=x&(-8, 6)abcd`, length of the ciphertext is e.g. 775
* If we are right:

`...user_data=token=a&token=abcd`

`...user_data=token=a&(-8, 7)bcd`, length of the ciphertext is e.g. 774

So, we can use this oracle to bruteforce the password 1 by 1 byte by observing the ciphertext lengths.

Simple, right? Unfortunately, both gzip and deflate also use huffman encodings on top of LZ77, making the exploit a bit harder. To make sure that only LZ77 affects the length, we need to add some padding to our input. There are two main methods of solving the problem with Huffman encodings:
1. The alphabet method

The alphabet method adds as a suffix to our guess the entire alphabet of possible characters excluding the one we are currently guessing separated by characters that for sure do not appear in the password (like "~"). Also this suffix is appended after another padding ("{}"), separating it from our payload e.g.:

`...user_data=token=b{}{}{}{}a~c~d[...]~z&token=abcd`

1. The two-tries method

The two tries method changes a bit the way in which we use the oracle. Instead of sending one guess for each letter and finding the one which ciphertext was 1 byte smaller, we will send two requests per each letter and see if the first one, that should compress better if we are right, is shorter than the second one, which is "random". It looks a bit like this:

* If we are wrong:

`...user_data=token=b{}{}{}{}&token=abcd`, `len = 779`
`...user_data=token={}{}{}{}b&token=abcd`, `len = 779`

* If we are right:

`...user_data=token=a{}{}{}{}&token=abcd`, `len = 774`
`...user_data=token={}{}{}{}a&token=abcd`, `len = 775`

Randomizing the padding length also helps with false negatives. 

## Applying breach to the challenge

The 404 error message of `forum-app` takes the `location` from the url and sends it along with the password, compressed then encrypted, through our packet sniffer. It is therefore a perfect attack vector.

The attack url prefix looks then like this:

`"https://localhost:5000/password="`

This will be then sent in a http request of the following form:

`image=<...>text=404: password=&password=secretpassword`

From this point, we proceed with CRIME/BREACH as described earlier. Implementation details are in `solve.py`. Getting the password took around 20 minutes on the online version --- local version takes about 5. Implementation can probably be optimized to be a bit faster.