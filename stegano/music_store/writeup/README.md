## Sample store writeup

### Hint to discover
```gobuster dir --url <address> --wordlist=<wordlist>```

Hint is in folder notes.

### Step 1  
Download all images and music from website.  

### Step 2  
Using exiftool get metadata from all images.  
```exiftool 1.jpg``` and so on...  
In Comment is Base64 to decode. Each one contains passphrase to get data from music sample.  

### Step 3 
Using steghide  
```steghide extract -sf 1.jpg``` and so on extract using passphrases from previous step.  

### Step 4
Combining all parts from extracted texts files "decipher" flag using cyberchef and ROT13 bruteforce.   
