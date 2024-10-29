













**The submission deadline is Monday, 2024-Nov-25.** Please note the [Submission Guidelines](home/Submission-Guidelines) of this course. Students must work independently, and provide their own results. In polybox, please use the same file naming conventions as in the previous assignment.

The **motivation for this assignment** is to explore the fundamentals of acoustic communication by using audible sound as a carrier for data transmission. 
This involves understanding how to embed data into sound through phase shifts and multi-frequency modulation. By examining this approach, we aim to grasp the potential and limitations of acoustic data transmission. 
Additionally, a key focus will be on best practices for data representation and visualization, enabling us to derive meaningful conclusions from the evaluation process.


# Step 1: Theory
<details><summary>Click to expand</summary>

For this step, reporting is not required.

Read through the Audio Communication lecture slides and the related background reading supplementary material on Audiocom:

 * H. Malvar, A modulated complex lapped transform and its applications to audio processing, 1999 IEEE International Conference (Vol. 3, pp. 1421-1424)
 * R. Frigg, T. R. Gross and S. Mangold, Multi-Channel Acoustic Data Transmission to Ad-Hoc Mobile Phone Arrays, July 2013, Association for Computing Machinery

Please think about the following questions, no report needed:
 * Does acoustic communication rely on electromagnetic waves? How fast do acoustic waves travel through air (estimate)?
 * When sampling at 10 kHz, what is the resolution that a time-of-flight distance measurement (also referred to as [time-of-arrival](https://en.wikipedia.org/wiki/Time_of_arrival)) could achieve in theory (estimate, leave out implementation details)? Think about how many samples per second are available, and what the precision in terms of time that means. Say, a signal is switched on and off, at what time precision can be a shift of this signal be detected? Once this is clear, transform time precision into distance. For this, remember the speed of an acoustic signal.
 * At this 10kHz sampling rate, what would be the precision with electromagnetic waves Remember that an electromagnetic signal travels much faster than an acoustic signal?
 * How would the distance precision change if the sampling rate is doubled to 20 kHz instead (for both, acoustic and electromagnetic waves)?
 * What is the typical bandwidth, measured in Hertz, of an acoustic sound recorded with a smartphone or a similar device?
 * What is the frequency range at which humans perceive sound (from ... to ..., measured in Hertz)?
</details>

# Step 2: Analyze Sound Files
<details><summary>Click to expand</summary>

#### Corresponding Notebook [AudioCommunication.ipynb](https://gitlab.ethz.ch/wireless/WirelessNotebooks/-/tree/main/AudioCommunication)

Start off by analyzing two sounds: *MobileComp1* and *MobileComp2*.

**Task**: answer the following questions:
 * Which sound file is more suited to carry the data? Why? Provide the visualizations and discuss them (time/frequency/spectrogram)
 * Which frequencies should be used to encode the data?

*Note*: the plotting of the spectrogram may take some time. If needed, you can reduce the `FFT_win_size` parameter, although this may impact the quality of the output.
</details>

# Step 3: Embed the message
<details><summary>Click to expand</summary>

Proceed with the notebook's section about Encoding.

**Task**: answer the following question:
 * Is there a perceivable change of the audio file? Does the sound quality remain?
 * Do you see a difference between the unembedded and embedded audio file's spectrogram? Could you conclude on the plot alone that it was done using phase coding? How would the plot look like for LSB coding?



</details>

# Step 4: Decode the message
<details><summary>Click to expand</summary>

Now, reconstruct the message from the embedded audio file and analyze the accuracy.

**Task**: answer the following question:
 * Are there bit errors? If yes, what might be the reason for them?
 * What does a bit error rate of 100%, 50%, and 0% mean? Which one is the least desirable?
 * Which of the two audio files (`MobileComp1`, `MobileComp2`) has a higher bit error rate? Was your initial guess correct?

</details>

# Step 5: Choose your own sound
<details><summary>Click to expand</summary>

Please think about the following questions, no report needed:
 * What could be some issues with audio steganography when used in a real life setting?
 * How would the perfect audio file for phase coding look like? What about the worst possible file?
 * Which results do you expect from the other audio files within `Sounds/`?

For this last step, please choose a new audio file (not from `Sounds/`) and briefly compare it to the previously used audio files.
As a help, section 3 of the notebook contains a cell that converts any audio file to the right format and configuration.
Please make sure that the chosen audio file has enough capacity for the message.

**Task**: answer the following question:
 * Which sound did you choose? Why?
 * How does your audio file measure up against `MobileComp1` and `MobileComp2` respectively?
 * What is the bit error rate?
 * How does it look like when changing the message to `manimatter`?

</details>

# Expected Results, all in one PDF


Please submit the following results (do not forget the visualizations), through ETH Polybox as one PDF document.

- Name and Legi number
- Step 1: (no report needed)
- Step 2: Visualizations (time/frequency/spectrogram) and answers to the questions
- Step 3: Answers to the questions (no visualizations)
- Step 4: Visualizations (spectrogram) and answers to the questions
- Step 5: Answers to the questions (no visualizations or audio files)
- OPTIONAL: feedback on the assignment: difficulty, clarity, time spent


<div align="center" width="100%">════════════

**Getting Help**
<br>[Course Overview](home)
<br>[Class Material](https://gitlab.ethz.ch/wireless/WirelessNetworkingAndMobileComputing/-/tree/main/Material)
<br>[Course @ ETH Zurich](https://www.lst.inf.ethz.ch/education/wireless.html)

**Assignments**
<br>[01](home/Assignment-01) [02](home/Assignment-02) [03](home/Assignment-03) [04](home/Assignment-04) [05](home/Assignment-05) [06](home/Assignment-06) [07](home/Assignment-07) [08](home/Assignment-08)
<br>[Submission Guidelines](home/Submission-Guidelines)
<br>[Use of Generative AI](home/Use-of-AI)
<br>[Background Reading](https://gitlab.ethz.ch/wireless/BackgroundReading)
<br>[Mobile Computing Notebooks](https://gitlab.ethz.ch/wireless/WirelessNotebooks)
<br>
════════════<br>
 Stefan Mangold<br>(stefan.mangold@inf.ethz.ch)<br><img width="200px" height="auto" src="uploads/e0009174c4495ec7500cc167cf53ccc6/eth_logo_kurz_pos.png"></div>
