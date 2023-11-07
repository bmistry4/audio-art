# Notes

- Visualisations require wav format
- To convert ogg to wav format requires using pydub
- To use pydub requires installing ffmpeg (follow https://www.wikihow.com/Install-FFmpeg-on-Windows)

TODO
- readme installation and usage
- requirements file
- interactive plots? embed in blog/ jupyter notebook? 

# Audio Art
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


- **Final Result:** See the final product [here](#canvas-print)! 


- **How?** Read this blog!

# The Data: Dealing with Audio
Let's first talk about the data we will work with - Audio. 
To understand how the art pieces are created requires knowing about the time and frequency domains. 
I'll explain it all below! 

## Back to basics: A wave 

---
### Handy (additional) resource(s): 
- Blog post: https://towardsdatascience.com/learning-from-audio-time-domain-features-4543f3bda34c
---

Audio signals are just waves, so let's consider a wave from a Physics perspective: 
![physics-wave.png](images%2Fblog%2Fphysics-wave.png)
From https://cdn1.byjus.com/wp-content/uploads/2023/03/Wave-Updated-1.png

From the above image, keep in mind the following points:
- The wave represents a **signal**
- **Time** domain: The axis is over time
- Repetition: A wave is a repeating pattern
  - One cycle is called an **oscillation** 
- **Frequency**: Is the number of oscillations per second, measured in hertz (Hz)
- **Amplitude/Power**: The height of the wave
  - Amplitude is the strength of the wave which is related to the **loudness** of a sound; higher amplitude means louder, lower amplitude means quieter

An audio signal is a wave that can be interpreted in either the **time domain** or the **frequency domain**.

## Time domain: Time vs Amplitude
Interpreting an audio signal in the time domain allows for a simple way to visualise the audio. 
The visualisation is a 2D plot showing how the amplitude of the audio signal changes over time. 
- x-axis (time): The audio clip will run for a certain amount of seconds 
- y-axis (amplitude): Refers to the sound intensity
  - Use the `scipy.io.wavfile` [(click for docs)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html) module to read the audio file. 
  - The returned data is given in a `numpy array` and the data type is dependent on the audio files bit-depth (the number of bits in each sample). 
  - For my case, I was dealing with a 32-bit integer PCM
    - PCM = pulse-code modulation. PCM is an uncompressed and lossless digital audio format.
    - (The data is not in decibels (a common unit of sound pressure level) but can be converted from 32-bit audio data to decibels.)

### Example plots
The time domain plot for my audio is shown below, where each minute's worth of data is coloured differently. 

![time_domain_full.png](images%2Ftime_domain_full.png)

One question you might be asking is why does the plot not look very much like a "sound wave"?
The answer is simply that there is a LOT of data points plotted every second. 
Every second, there are 48,000 data points to plot and this is called the **sample frequency**. 
For the audio clip I used, there's 45,025,816 data points (with the full clip being ~983 seconds long). 
That's a lot of points to plot! 

To convince you, let me zoom into the plot and consider only the first 10 seconds worth of data...

![time_domain_10s.png](images%2Ftime_domain_10s.png)

Looks more like a classic sound wave right? 
If we really zoom in and only consider the first 0.001 seconds of data then we can even see a wave!

![time_domain_1e-3s.png](images%2Ftime_domain_1e-3s.png)

That's everything you need to know about the time domain. 
Now, let's talk about the frequency domain.

## Frequency domain: Frequency vs Amplitude 

---
### Handy (additional) resource(s): 
- Excellent blog: https://realpython.com/python-scipy-fft/
- Video for visual learners (3Blue1Brown): https://www.youtube.com/watch?v=spUNpyF58BY&t=835s
- Short video explanation (with maths): https://www.youtube.com/watch?v=8V6Hi-kP9EE&t=207s
---
Another way to consider a signal is in the frequency domain. 
To get there, we need to apply the Fourier Transform (FT). 

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

If you about music, think of the FT as transforming the sound of a chord into its constituent pitches of different intensities. 

Not only can you go from the time domain to frequency domain, you can also go the other way around since the 
transformation is invertible (i.e., inverse FT)! 

### How does it work? TODO
There are two types of FT, the continuous FT (CFT) and the discrete FT (DFT). The

### What's the FAST Fourier Transform (fft)
The FFT is an algorithm to calculate the DFT. As the name implies, it's fast to compute so is used alot in practice. 

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
This is no coincidence, and is equal to the **Nyquist frequency** for the signal. 
The Nyquist frequency is a well known concept in signal processing and represents half the sampling rate of a discrete signal. 

### Polar Coordinates - What Are They? 
If I asked you to plot the point (2,3) on a 2-dimensional axis you'd probably draw a cross to represent the X-Y axes and
then plot a point that is 2 to the left and 3 up of the origin (0,0). If that's what you did then congratulations, 
you're working with **cartesian coordinates**! 

Now **polar coordinates** provide an alternative way to represent the position of a point in a plane.
Instead of using the x and y coordinates for a point’s position like in cartesian coordinates, polar coordinates use a 
**magnitude** r and **phase** θ. 
A point P is defined by (r,θ), where r is the distance from the origin and the θ is an angle (measured in degrees/radians) 
starting from the origin pointing in positive x-axis direction to the point P. 
You can convert between the cartesian and polar coordinates, but that is out of the score of this blog. 

There can be cases where it's easier to represent/interpret data using polar coordinates than cartesian, so it's handy 
to know about! One such case is complex numbers which is exactly the kind of values return by applying the FFT. 


# The Art: Making Asethetic Looking Pictures
_Keeping to the mindset of 'it's not a bug, it's a feature' but for an art context - 'it's not ugly, it's intentional"_,
I had two personal criteria when creating the art:

1) Make it look nice
2) Make it meaningful

Since first is subjective, I'll just my gut instinct. 
The second is because I want this art piece to be a memorable gift. 

## Making the data sparse
A problem I encountered early on was the issue of dealing with the masses of data points. 
The audio clip was nearly 16 mins of data with a sample rate of 48000 Hz. 
That means for each second there was 48,000 separate data points, meaning I had to somehow express ~45 million data 
points into a single image. 
To deal with this, I had a spasification step to reduce the number of data points. 
This step will be used in all the art pieces. 
I considered three ways: 
1) `random`: drop random points until you're within a max sample threshold
2) `drop`: drop every other point repeatedly until you're within a max sample threshold
3) `window-and-random`: take an average over a non-overlapping sliding window
   - The window size is `data // max_samples`
   - If the window size is 1 then just use the `random` method to drop data points


## Funky Frequency Waves
**Motivation**: Since audio signals are all about waves, my first go to was to create overlapping waves be analogous to the hills in the mountain. 
I wanted to keep in the time domain for this one. 
That way you see the changes in the voice over time which would represent the challenge of climbing up a mountain.
I envisioned something like breaking the audio clip into small intervals and plotting each interval using time vs amplitude. 
Each interval would be stacked ontop of eachother since having them all one after another would be too long horizontally. 

### Stack plot with smoothing
To create the overlapping effect, I used a [stack plot](https://python-graph-gallery.com/streamchart-basic-matplotlib/). 
The 1st subplot below looks very spiky, so to smooth it out you can use a Gaussian Kernel. 
For a more rigorous smoothing, you can also use a grid version of Gaussian smoothing where the weights for smoothing 
are across a grid of coordinates rather than just around the x-coordinates. 
Now we're getting somewhere!

![0-gaussian.png](images%2Ffreq-waves-overlapping%2F0-gaussian.png)

### Colour and Transparency
Ok, let's add some colour and transparency. 
For colouring, we'll define a colour to start at and a colour to end at and interpolate between them so each bin (wave)
has its own colour. Let's also do the same for transparency aswell (starting at 0.8 and reducing to 0.4).

![1-gaussian-cols-alphas.png](images%2Ffreq-waves-overlapping%2F1-gaussian-cols-alphas.png)

### Stackplot Baseline Argument
The matplotlib stackplot has a parameter called `basline` which controls where the stacking happens. Options include: 
- `zero` (default) = have a baseline at y=0 and stack on there. 
- `wiggle` = minimizes the sum of the squared slopes
- `sym` = like zero, but is symmetric

Let's see what these do to the image: 

![2-gaussianBaselines-cols-alphas.png](images%2Ffreq-waves-overlapping%2F2-gaussianBaselines-cols-alphas.png)

I like the sym option best, so will use it for the remaining options. 

### Sparsity Methods
At this point, can see the intricacies of the layered waves quite nicely thanks to the colouring and transparency. 
Hence, it's a good time to see the effect of the different sparsity methods I mentioned [earlier](#making-the-data-sparse). 
So far, the above plots have been using the "random" method. 
If we compare all three methods we see that each will give quite a different result! 

![3-gaussianBaselines-cols-alphas-sparsify.png](images%2Ffreq-waves-overlapping%2F3-gaussianBaselines-cols-alphas-sparsify.png)


### Additional Parameters 
Let's now look at 5 different parameters which can greatly influence the look of the picture. They are the gaussian 
standard deviation and gaussian offset, the number and size of the bins, and the colouring of the plot. 
The best choice for these parameters are completely subjective so will vary for each person. 

The standard deviation used for the Gaussian smoothing controls will control how smooth the waves will look like. 
The larger the standard deviation, the smoother the wave:

![4-gaussianSym-sdev.png](images%2Ffreq-waves-overlapping%2F4-gaussianSym-sdev.png)

The Gaussian offset is used when generating the grid for smoothing. It controls how much to offset the min and max 
values of the grid compared to the domain of the x-values. 
You'll find that negative offset values stretch out the waves, while positive values will close at the tips: 

![5-gaussianSym-gaussianOffset.png](images%2Ffreq-waves-overlapping%2F5-gaussianSym-gaussianOffset.png)

To get different waves to overlap, I would chunk the data into equal sized bins. 
Changing the number of bins controls the number of different waves we want stacked together: 

![6-gaussianSym-binsNum.png](images%2Ffreq-waves-overlapping%2F6-gaussianSym-binsNum.png)

And changing the size of the bin controls how many data points can be used to define a single wave. 
A larger size means more points so more fluctuating waves. 

![7-gaussianSym-binsSize.png](images%2Ffreq-waves-overlapping%2F7-gaussianSym-binsSize.png)

Finally, we can also try out different colour schemes: 

![8-gaussianSym-colours.png](images%2Ffreq-waves-overlapping%2F8-gaussianSym-colours.png)

[//]: # (With all the different options in mind, this was my final choice for this art piece: )

[//]: # (**Parameters**)

[//]: # (- stack plot)

[//]: # (  - baseline: wiggle)

[//]: # (- smoothing)

[//]: # (  - type: grid gaussian)

[//]: # (  - std dev: 15)

[//]: # (  - offset: 50)

[//]: # (- sparsity: window-and-random)

[//]: # (- bins)

[//]: # (  - number: 30)

[//]: # (  - size: 500)

[//]: # (- colours: &#40;"#ed5394", "#eda253"&#41;)

[//]: # (- alphas: [0.8, 0.4])

[//]: # ()
[//]: # (![final-frequency-waves-overlapping_dep-600.png]&#40;images%2Ffreq-waves-overlapping%2Ffinal-frequency-waves-overlapping_dpi-600.png&#41;)

## Turning Polar: Revolving Beams
**Motivation**: Instead of waves which are sequential, how about something a bit more circular. 
So plot points going around a circle, over and over again. 
Since the FFT returns _complex numbers_ it naturally allows us to dabble with polar plots since complex numbers can 
also be expressed as [polar coordinates](#polar-coordinates---what-are-they-)!
Converting the complex numbers from the cartesian form to the polar form results in a magnitude and phase for each data point. 

### Basic Polar Plot
To start, assume the data has been preprocessed using the `random` sparsification technique mentioned earlier.  
Now, let's look at the 4 incremental steps to create the figure. 

1) Plot a polar bar chart using only the default configuration. It won't look too great; 
you can't see any of the individual bars and the figure looks a bit like a distorted circle. 
2) Add some transparency by setting the `alpha` parameter to 0.4. We start seeing some details, but the center 
still looks very dense. 
3) Instead of having the `width` (=0.8) the same for each bar, let's grow it linearly with each point being plotted,
i.e., `width=np.linspace(np.pi / 32, np.pi / 8, len(theta))`. Now we're getting somewhere. 
4) To top it all off, let's add some colours which will start "#8d7ed8" and end at "#5bffef" using linear interpolation. 

With these steps we successfully have created some polar art! 

![0-baseline.png](images%2Fpolar-slices%2F0-baseline.png)

### Additional Parameters 
There's a couple of parameters you can play around with. 

For example, the sparsify method when preprocessing the data:

![1-sparsify-methods.png](images%2Fpolar-slices%2F1-sparsify-methods.png)

The total number of data samples to plot: 

![2-max-samples.png](images%2Fpolar-slices%2F2-max-samples.png)

The colours to use: 

![3-colours.png](images%2Fpolar-slices%2F3-colours.png)


The amount of transparency to set: 

![4-alphas.png](images%2Fpolar-slices%2F4-alphas.png)

Allowing the y-axis (representing magnitude) to use a log axis:

![5-alphas-logY.png](images%2Fpolar-slices%2F5-alphas-logY.png)


[//]: # (With all these in mind, my final choice was the following: )

[//]: # (![final-polar-slices_dpi-600.png]&#40;images%2Fpolar-slices%2Ffinal-polar-slices_dpi-600.png&#41;)

## Turning Polar: Floral Vibes 
**Motivation**: I like the look of the polar plot, but I wanted something a bit softer for the shape of the bars, 
like petals to give it some floral-like look. I also wanted the image to look more busy and dynamic to try to represent 
the different emotions that may have occurred while the person who recorded this audio felt while hiking. 

To make the bars of the previous plots look more like petals, you can plot coloured in Bézier curves using the matplotlib's `PathPatch`. 
Each PathPatch will take a Path that tells you how to draw a petal from 4 points (start point, 2 control points and an end point). 
Like before, we'll use different colours and transparencies to make a nice layered effect.

### Centerpiece: Lapsing Emotions
First let's get something similar to what I just described: 

1) Plot bars in shape of petals. Below is an example of drawing 2 petals
2) Plot all the petals for the full preprocessed audio. So far, it'll look like a bumpy circle.
3) Add colour to each petal. We still can't see too many petals though...
4) Add a fixed amount transparency (=0.4) to all petals. Now we can see some layering. 
5) Use adaptive transparencies so each bin of data will be less transparent. Results in a nice fade out effect.
6) Instead of having the width (=0.8) the same for each point, let's grow it linearly with each point being plotted, 
i.e., width=np.linspace(np.pi / 32, np.pi / 8, len(theta)).
7) (Extra) Colour in the edges rather than the petals.

![0-baseline.png](images%2Fpolar-floral-full%2F0-baseline.png)

Now we've got a good starting point, let's play around with some parameters!...

When drawing the petals, we can change how far from the origin we plot from. 
Increasing this offset can result in a small hole in the center of the figure. 
We can also have adaptive offset values, which mean the offset will linearly increase with each new bin of data to plot. 

![1-radii-offset.png](images%2Fpolar-floral-full%2F1-radii-offset.png)

Using different methods to make the data sparse:

![2-sparsify.png](images%2Fpolar-floral-full%2F2-sparsify.png)

Normalising the audio data after it's been fourier transformed:

![3-norm.png](images%2Fpolar-floral-full%2F3-norm.png)

Adapting the number of bins:

![4-binsNum.png](images%2Fpolar-floral-full%2F4-binsNum.png)

Or the number of data samples in a bin:

![5-binsSize.png](images%2Fpolar-floral-full%2F5-binsSize.png)

And there's always the choice of the colour scheme! 

![6-colours.png](images%2Fpolar-floral-full%2F6-colours.png)

[//]: # (The final product looks like this! )

[//]: # (![final-polar-floral-center-round_dpi-600.png]&#40;images%2Fpolar-floral-full%2Ffinal-polar-floral-center-round_dpi-600.png&#41;)

### Capturing minutes: Floral Border
**Motivation** The centerpiece images above looks like a neat piece containing data from the full length clip. 
But I feel something a bit more fine-grained, like having a image representing ever minute-or-so would be a nice touch. 
So let's make a circular border which has small flower-like images, where each flower represents a minute of data. 
I've made some slight changes to what the image represents. 
- Each flower represents a small chunk of audio. (I'll use 16 flowers to represent each minute of my 16-minute audio.)  
- The radius from the polar coordinates is still used to determine the length of the petal
- The width of the petal is fixed to pi/8  
- The theta of the polar coordinates is no longer used. Instead, the data is plotted in order in an anticlockwise fashion.
So, the start of the audio is at angle 0 degrees and the end of the audio would have done the full loop and be at 360 degrees.

Now let's look at some examples.
First see how the flowers are organised; you get an evenly spaced out circular border: 

![3-binsNum.png](images%2Fpolar-floral-segments-circle%2F3-binsNum.png)

Using the different data sparsity methods:
 
![1-sparsify.png](images%2Fpolar-floral-segments-circle%2F1-sparsify.png)

Increasing the radii offset: 

![2-radii-offset.png](images%2Fpolar-floral-segments-circle%2F2-radii-offset.png)

Changing the number of allowed datapoints to represent a single flower (i.e., bin size):

![4-binSize.png](images%2Fpolar-floral-segments-circle%2F4-binSize.png)

And finally, different colour schemes:

![5-colours.png](images%2Fpolar-floral-segments-circle%2F5-colours.png)

[//]: # (The final result: )

[//]: # (![final-polar-floral-segments-circle_dpi-600.png]&#40;images%2Fpolar-floral-segments-circle%2Ffinal-polar-floral-segments-circle_dpi-600.png&#41;)

### Combining components - Floral Border and Center 
**Motivation**: I thought it would be a nice to have a piece which had both the fine-grained boarder data which 
showed a flower for each minute's worth of data and also have a centerpiece which represented the entire length of 
audio in a single image. 

![final-polar-floral-borderAndCenter_dpi-600.png](images%2Fpolar-floral-border-and-center%2Ffinal-polar-floral-borderAndCenter_dpi-600.png)


# QR Code - Scannable Art! 

---
Handy (additional) resource(s): 
- Article explaining more details on using qrcode: https://medium.com/@reegan_anne/fully-customizable-qr-codes-in-python-7eb8a7c3b0da)
---

Now for the cherry on top! 
Since the art was created from an audio sample let's add a QR code component which we can scan to get us to the audio 
clip!
<span style="color: red;">NOTE: Since the art pieces I've shown have been created using a private audio clip, 
I'll instead set the QR link to my website.</span>

Conveniently, there already exists a QR code generator library called `qrcode` (https://github.com/lincolnloop/python-qrcode)! 
There's some neat features which we'll use from it including: 
- Having a link to some website/link/text (your choice!)
- Having a center image
- Having a background image underneath the qr code
- Having different qr code styles (module drawers)


Just generating the QR code to the link will look like this: 

![qrcode_bkgNone_logoNone_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgNone_logoNone_dpi-600_VerticalBarsDrawer.png)


Now, let's take floral center and border art piece from earlier add it to the center: 

![qrcode_bkgNone_logoFloralBorderAndCenter_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgNone_logoFloralBorderAndCenter_dpi-600_VerticalBarsDrawer.png)

Ok, looks a bit bland...let's fix that! 
What if we used it as the background image instead of having it in the center? 

![qrcode_bkgFloralBorderAndCenter_logoNone_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgFloralBorderAndCenter_logoNone_dpi-600_VerticalBarsDrawer.png)

It makes it difficult to see the centerpiece, but the border doesn't look too shabby. Let's just use the border as the background instead: 

![qrcode_bkgFloralBorder_logoNone_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgFloralBorder_logoNone_dpi-600_VerticalBarsDrawer.png)

You can't see much of the border, so let's use a "thicker" border which had a smaller radius: 

![qrcode_bkgFloralThickBorder_logoNone_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgFloralThickBorder_logoNone_dpi-600_VerticalBarsDrawer.png)

Better! Now let's add back in a center image but use a version which does not have a floral border: 

![qrcode_bkgFloralThickBorder_logoFloralCenter_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgFloralThickBorder_logoFloralCenter_dpi-600_VerticalBarsDrawer.png)

Or instead, let's use a different center image... maybe one of the funky frequency waves? 

![qrcode_bkgThickFloralBorder_logoWaves_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgThickFloralBorder_logoWaves_dpi-600_VerticalBarsDrawer.png)

And voilà! A lovely piece of art which can be scanned! 
The qrcode library also gives you options to play around with the qrcode style by modifying the `module_drawer` argument
for the `makr_image` method. Options include: `RoundedModuleDrawer`, `CircleModuleDrawer`, `VerticalBarsDrawer`, 
`SquareModuleDrawer`, `HorizontalBarsDrawer`, and `GappedSquareModuleDrawer`. 
The qrcodes you've been seeing have been using the `VerticalBarsDrawer`. 
Using the others will result in the following: 

![qrcode_bkgThickFloralBorder_logoWaves_dpi-600-ModuleDrawers.png](images%2Fqrcode%2Fblog%2Fsave%2Fmodule_drawer%2Fqrcode_bkgThickFloralBorder_logoWaves_dpi-600-ModuleDrawers.png)

You may have noticed the thick black borders around the QR codes. 
I needed this because I ended up printing this qrcode onto a canvas. I wanted the canvas to have wrapped edges 
so need this thick border to avoid the qrcode being wrapped around the edges when printed. 

# Canvas Print
For those interested, I used https://www.photobox.co.uk/ to print and deliver my canvas. Specifically I created a 
square 30x30cm canvas print with the wrap (edges) option (https://www.photobox.co.uk/shop/canvas-prints/simple-canvas).
The printed canvas looked pretty great and the scan worked perfectly! 

Here's it is (<span style="color: red;">I added markings on the code to stop the scan from working since it's for private use only)</span>: 

TODO ADD CANVAS IMG

_Just in time for Christmas! :D_

# Conclusion
A there we have it! 
We've covered how convert an audio clip to different pieces of art and even add make it scannable using QR codes! 
If you want to try it on your own audio files be my guest! You can find all the code available at https://github.com/bmistry4/audio-art! 

Enjoy :) 
