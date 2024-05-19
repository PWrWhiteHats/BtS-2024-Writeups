To retrieve the hidden flag, you should downloads the song from the credits using any tool like https://notube.net/pl
Then trim the audio file to 19 seconds, just like the banger.wav audio file nd change it to wav format. (I use capcut)
Then cut the sound of the exported song from the banger file to get the sound containing the flag.
example solution:
```
    fnames =["./rickroll.wav", "./banger.wav"]
    wavs = [wave.open(fn) for fn in fnames]
    frames = [w.readframes(w.getnframes()) for w in wavs]
   
    samples = [np.frombuffer(f, dtype='<i2') for f in frames]
    samples = [samp.astype(np.float64) for samp in samples]
  
    n = min(map(len, samples))
    mix = samples[1][:n] - samples[0][:n]
    # Save the result
    mix_wav = wave.open("./flag.wav", 'w')
    mix_wav.setparams(wavs[1].getparams())

    mix_wav.writeframes(mix.astype('<i2').tobytes())
    mix_wav.close()
```
There are many spectrum analyzers online, so there is no fear example https://academo.org/demos/spectrum-analyzer/ 
When you use the analyzer spectrum a flag will appear.

