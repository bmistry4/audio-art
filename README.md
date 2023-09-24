# Notes

- Visualisations require wav format
- To convert ogg to wav format requires using pydub
- To use pydub requires installing ffmpeg (follow https://www.wikihow.com/Install-FFmpeg-on-Windows)

# TODO
- create private github with audio file and give access to fam. 
- Create qr code which is linked to file 
- add qr code to iamge
---
# Blog
# Static Audio Art
Turning a spoken memory into art.

- **What?** Turn an audio clip into a piece of static art.


- **Why?** (Motivation/Background story.) A few months ago, someone close to me had gone on a holiday to Wales, 
specifically, to climb Mount Snowdon. (Snowdon is the highest mountain in Wales, with a height of 1,085m!) On a good day 
this is a mighty LONG trek (~5-7 hrs), so as you can imagine, on a stormy day this is a might LONG and HARD trek. 
With it being the typical British weather, of course there was a storm, and with this person's luck, of course it 
was a big one (Storm Antoni to be specific)! Long story short nothing of theirs went to plan. This included the weather, 
the time of the hike, finding the spare torch batteries, finding the train to back down the mountain, or remembering their 
toothbrush during their stay! But even with all those setbacks and awful conditions, they still managed to do the hike! 
After completing the hike (and regaining the feeling in their fingers), I was sent an audio message (~15-16 mins long) 
explaining their journey from start to end. Listening to their monologue, I thought "Wow, what a journey and heck of an 
experience!". I wanted to make something personal for them as a reminder of their little adventure, and since art is 
fun and expressive I thought why not!


- **How?** Now we get to the good (technical) stuff!

# The Data: Dealing with Audio

- Conversion between ogg to wav: Before even getting to analyse the data, I had to convert it to the correct format. 
- An audio signal can be interpreted in either the time domain or the frequency domain. (We will go through both a bit later!)

## Back to basics: A wave 
https://towardsdatascience.com/learning-from-audio-time-domain-features-4543f3bda34c

To start, let's consider of a simple wave from a Physics perspective...

![physics-wave.png](images%2Fblog%2Fphysics-wave.png)
From https://cdn1.byjus.com/wp-content/uploads/2023/03/Wave-Updated-1.png

Keep in mind the following points:
- The wave represents a **signal**
- **Time** domain: The axis is over time
- Repetition: A wave is a repeating pattern
  - One cycle is called an **oscillation** 
- **Frequency**: Is the number of oscillations per second, measured in hertz (Hz)
- **Amplitude/Power**: The height of the wave
  - Amplitude is the strength of the wave which is related to the **loudness** of a sound; higher amplitude = louder, lower amplitude = quieter

## Time domain: Time vs Amplitude
This is a simple way to visualise the audio and is plotted on a 2D axis. 
The plot visualises how the amplitude of the audio signal changes over time. 
- x-axis (time): The audio clip will run for a certain amount of seconds 
- y-axis (amplitude): Refers to the sound intensity
  - We use the `scipy.io.wavfile` [(click for docs)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html) module to read the audio file. 
  - The returned data is given in a numpy array and the data type is dependent on the audio files bit-depth (the number of bits in each sample). 
  - For this case, I was dealing with a 32-bit integer PCM
    - PCM stands for pulse-code modulation and is an uncompressed and lossless digital audio format.
    - The data is not in decibels (a common unit of sound pressure level) but can be converted from 32-bit audio data to decibels.

Q) What does it mean to have a negative amplitude?

### Example plots
Doing a time domain plot for my audio would look like the plot below, where each minute's worth of data is coloured differently. 

![time_domain_full.png](images%2Ftime_domain_full.png)

Now, one question you might be asking is why does the plot not look very much like a sound wave. 
The answer is simply that there is a lot of data points plotted every second. 
Every second, there are 48,000 data points to plot and this is called the sample frequency. 
For the entire clip there's 45,025,816 data points (with the full clip being ~983 seconds long). 
That's a lot of points to plot! 

To convince you, let me zoom into the plot and consider only the first 10 seconds worth of data...

![time_domain_10s.png](images%2Ftime_domain_10s.png)

Looks more like a classic sound wave right?!
And since at the end of the day, the audio signal is just a wave, if we really zoom in and only consider the first 0.001 
seconds of data then we can even see a wave...

![time_domain_1e-3s.png](images%2Ftime_domain_1e-3s.png)

That's about it for the time domain. Now, let's talk about the frequency domain.

## Frequency domain: Frequency vs Amplitude - The Fourier Transform
### Handy (additional) resources 
- Excellent blog: https://realpython.com/python-scipy-fft/
- Video for visual learners (3Blue1Brown): https://www.youtube.com/watch?v=spUNpyF58BY&t=835s
- Short video explanation (with maths): https://www.youtube.com/watch?v=8V6Hi-kP9EE&t=207s

### What is the Fourier Transform (FT)?
The FT is pretty neat. It can take a signal and tells you the simple (sin/cos) waves that make it up.
The resulting simple waves can be expressed solely by their frequency and amplitude values.

You can plot these to visualise how the amplitudes of the signal changes over the different frequencies. 
Hence, the FT takes a signal (representing a function in the time domain) and transforms it into the frequency domain. 

<p align="center">
  <img src="images/blog/fourier-transform.gif" />
</p>

[//]: # (![fourier-transform.gif]&#40;images%2Fblog%2Ffourier-transform.gif&#41;)
(source: https://en.wikipedia.org/wiki/Frequency_domain)

[//]: # (https://en.wikipedia.org/wiki/File:Fourier_transform_time_and_frequency_domains_&#40;small&#41;.gif)

Wikipedia provides this handy gif for a visual intuition on what the fourier transform does. 
The red signal is the original function in the time domain. Applying the FT you breakdown the red signal into multiple
blue waves of different frequencies. Taking the amplitude of each blue wave and plotting it in the frequency domain you're done! 

If you know a bit about music think of the FT as transforming the sound of a chord into its constituent pitches of different intensities. 

Not only can you go from the time domain to frequency domain, you can also go the other way around since the transformation is invertible (i.e. inverse FT)! 

### How does it work? 
There are two types of FT, the continuous FT (CFT) and the discrete FT (DFT). The

### What's the FAST Fourier Transform (fft)
The FFT is an algorithm to calculate the DFT. As the name implies, it's fast to compute. 

### Why is it useful?

### Example plots
You can use scipy to calculate the DFT using the FFT:

![frequency_domain_full.png](images%2Ffrequency_domain_full.png)

Applying the FFT will return an array of complex values representing the amplitude and phase of a sinusoidal component at a corresponding frequency.
Notice the symmetry about the Y-axis (amplitude axis). 
This **conjugate symmetry** in the frequency domain, is a result of the FFT being applied to a real-valued signal. 
An explanation is shown [here](https://dsp.stackexchange.com/a/4827).
Due to this property, you can just plot the positive X-axis domain like below:

![frequency_domain_full_positiveXonly.png](images%2Ffrequency_domain_full_positiveXonly.png)

One last thing. See how, in the x-axis for the above figures, the highest frequency is at 24,000 Hz (i.e., half the sampling rate).
This is no coincidence, and is equal to the  Nyquist frequency for the signal. 
The Nyquist frequency is a well known concept in signal processing and represents half the sampling rate of a discrete signal. 

TODO - what is the Nyquist frequency

# The Art: Making Asethetic Looking Pictures
_Keeping to the mindset of 'it's not a bug, it's a feature' but in an art context - 'it's not ugly, it's intentional"_,
I had three criteria when creating this art:

1) Make it look nice
2) Make it meaningful
3) Limit the amount of data that is thrown away 

The first is subjective, but I decided to follow my gut instinct. 
The second is because I want this art piece to be memorable, so having meaning as to why I made it the way I did is a good sign. 
The third, is to avoid transforming the data too much. 

## Funky Frequency Waves
Since audio signals are all about waves, my first go to was to create overlapping waves be analogous to the hills in the mountain. 
I wanted to keep in the time domain for this one. 
That way you see the changes in the voice over time which would represent the challenge of climbing up a mountain.
I envisioned something like breaking the audio clip into small intervals and plotting each interval using time vs amplitude. 
Each interval would be stacked ontop of eachother since having them all one after another would be too long horizontally. 

A problem I encountered early on was the issue of dealing with the masses of data points. 
The audio clip was nearly 16 mins of data with a sample rate of 48000 Hz. 
That means for each second there was 48,000 separate data points, meaning I had to somehow express ~45 million data 
points into a single image. I considered three ways: 1) drop random points, 2) drop every other point repeatedly, or 3) 
take an average over a window. 
TODO - EXPLAINNNN

To create the overlapping effect, I used a [stack plot](https://python-graph-gallery.com/streamchart-basic-matplotlib/). 
The plot looks very spiky, so to smooth it out you can use a Gaussian Kernel. 
For a more rigorous smoothing, you can also use a grid version of Gaussian smoothing where the weights for smoothing 
are across a grid of coordinates rather than just around the x-coordinates. 
Now we're getting somewhere!

![0-gaussian.png](images%2Ffreq-waves-overlapping%2F0-gaussian.png)

Ok, let's add some colour and transparency. 

For colouring, we'll define a colour to start at and a colour to end at and interpolate between them so each bin (wave)
has its own colour. Let's also do the same for transparency aswell (starting at 0.8 and reducing to 0.4).

![1-gaussian-cols-alphas.png](images%2Ffreq-waves-overlapping%2F1-gaussian-cols-alphas.png)

The matplotlib stackplot has a parameter called `basline` which controls where the stacking happens. Options include: 
- `zero` (default) = have a baseline at y=0 and stack on there. 
- `wiggle` = minimizes the sum of the squared slopes
- `sym` = like zero, but is symmetric

Let's see what these do to the image: 

![2-gaussianBaselines-cols-alphas.png](images%2Ffreq-waves-overlapping%2F2-gaussianBaselines-cols-alphas.png)

Each has its unique take. I'm liking sym the best, so the remaining images below will use it! 

Earlier I mentioned the need to make the data more sparse. 
So far, the above plots have been using the "random" method. 
Let's also see the other two methods in action: 

![3-gaussianBaselines-cols-alphas-sparsify.png](images%2Ffreq-waves-overlapping%2F3-gaussianBaselines-cols-alphas-sparsify.png)

Each sparisty method gives quite a different result as expected!
(Random is still my personal fav.)

Let's now look at 5 different parameters which can influence the look of the picture. They are the gaussian 
standard deviation and gaussian offset, the number and size of the bins, and the colouring of the plot. 
The choice for these parameters are completely subjective so will vary for each person. 

The standard deviation used for the Gaussian smoothing controls will control how smooth the waves will look like. 
The larger the standard deviation, the smoother the wave:

![4-gaussianSym-sdev.png](images%2Ffreq-waves-overlapping%2F4-gaussianSym-sdev.png)

The Gaussian offset is used when generating the grid for smoothing. It controls how much to offset the min and max 
values of the grid compared to the domain of the x-values. The offset looks something like this: 

Let's test out some different values...

![5-gaussianSym-gaussianOffset.png](images%2Ffreq-waves-overlapping%2F5-gaussianSym-gaussianOffset.png)

Negative values stretch out the waves, while positive values will close in the tips. 

To get different waves to overlap, the data was chunked up and put into bins. 
Changing the number of bins controls the number of different waves we want stacked together: 

![6-gaussianSym-binsNum.png](images%2Ffreq-waves-overlapping%2F6-gaussianSym-binsNum.png)

And changing the size of the bin controls how many data points can be used to define a single wave. 
A larger size means more points so more fluctuating waves. 

![7-gaussianSym-binsSize.png](images%2Ffreq-waves-overlapping%2F7-gaussianSym-binsSize.png)

Finally, there's the colouring: 

![8-gaussianSym-colours.png](images%2Ffreq-waves-overlapping%2F8-gaussianSym-colours.png)

With all the different options in mind, this was my final choice for this art piece: 
**Parameters**
- stack plot
  - baseline: wiggle
- smoothing
  - type: grid gaussian
  - std dev: 15
  - offset: 50
- sparsity: window-and-random
- bins
  - number: 30
  - size: 500
- colours: ("#ed5394", "#eda253")
- alphas: [0.8, 0.4]

![final-frequency-waves-overlapping.png](images%2Ffreq-waves-overlapping%2Ffinal-frequency-waves-overlapping.png)

## Turning Polar: Revolving Beams
Instead of waves which are sequential, how about something a bit more circular. 
So plot points going around a circle, over and over again. 
Since the FFT returns _complex numbers_ it naturally allows us to dabble with polar plots since complex numbers can 
also be expressed as polar coordinates! 

TODO - expln polar


Since we convert the complex numbers from the cartesian form to the polar form we get the magnitudes and phases for each data point. 
To start, assume the data has been preprocessed using the `random` sparsification technique we mentioned earlier.  
Now, let's look at the 4 steps to get our figure. 

1) Plot a polar bar chart using only the default configuration. It won't look too great. 
You can't see any of the individual bars and the end product just looks like a distorted circle. 
2) Add some transparency by setting the `alpha` parameter to 0.4. We start seeing some details, but the center 
still looks very dense. 
3) Instead of having the `width` (=0.8) the same for each point, let's grow it linearly with each point being plotted,
i.e., `width=np.linspace(np.pi / 32, np.pi / 8, len(theta))`. 
Now we're getting somewhere. 
4) To top it all off, let's add some colour which will start and end at `("#8d7ed8", "#5bffef")`. 

With these steps we successfully have created some polar art! 

![0-baseline.png](images%2Fpolar-slices%2F0-baseline.png)

There's a couple of parameters you can play around with. 
For example, the sparsify method when preprocessing the data ...

![1-sparsify-methods.png](images%2Fpolar-slices%2F1-sparsify-methods.png)

The total number of data samples to plot: 

![2-max-samples.png](images%2Fpolar-slices%2F2-max-samples.png)

The colours to use: 

![3-colours.png](images%2Fpolar-slices%2F3-colours.png)


The amount of transparency to set: 

![4-alphas.png](images%2Fpolar-slices%2F4-alphas.png)

If the y-axis (representing magnitude) should use a log axis:

![5-alphas-logY.png](images%2Fpolar-slices%2F5-alphas-logY.png)


With all these in mind, my final choice was the following: 

![final-polar-slices.png](images%2Fpolar-slices%2Ffinal-polar-slices.png)


## Turning Polar: Floral Vibes 
### Centerpiece: Lapsing Emotions

![0-baseline.png](images%2Fpolar-floral-full%2F0-baseline.png)
![1-radii-offset.png](images%2Fpolar-floral-full%2F1-radii-offset.png)
![2-sparsify.png](images%2Fpolar-floral-full%2F2-sparsify.png)
![3-norm.png](images%2Fpolar-floral-full%2F3-norm.png)
![4-binsNum.png](images%2Fpolar-floral-full%2F4-binsNum.png)
![5-binsSize.png](images%2Fpolar-floral-full%2F5-binsSize.png)
![6-colours.png](images%2Fpolar-floral-full%2F6-colours.png)
![final-polar-slices.png](images%2Fpolar-floral-full%2Ffinal-polar-slices.png)

### Border: Capturing minutes

# The Final Piece: Canvas Art
_Just in time for Christmas!_