# BaiBai Go — Midterm Presentation Script

Total: about 1366 words, 10 minutes. Speakers are suggestions; replace Member A–E with real names.

## Slide 1 — Title

**Time:** 0:20  |  **Suggested speaker:** Member E  |  **Words:** 62

Good morning, everyone. Our final project is called BaiBai Go, a voice-first temple route companion for seniors. "Bai-bai" is how people in Taiwan say going to the temple to pray. In the next ten minutes we will introduce the problem, the methods we plan to use, how our five members share the work, and how the project connects to the USR competition.

## Slide 2 — Seniors want to visit temples, but the trip is hard

**Time:** 1:20  |  **Suggested speaker:** Member E  |  **Words:** 180

Many seniors in Taiwan love going to the temple. It is a habit, a social event, and for many of them it is the main reason to leave the house. But they often give up, for three simple reasons: they are not sure about the route, there are too many stairs, or they are afraid it is too far to walk. When they stop going, they also lose exercise and social contact.

A map app could help, but typing and reading small text is difficult for them. Voice is the most natural interface: just say, "I want to go to the temple."

However, a voice assistant often fails in exactly this situation. Outdoors there is traffic, wind and temple music. Seniors often speak softly or hold the phone far away. And many of them have age-related hearing loss, so they cannot clearly hear the spoken answer.

So our problem is not only route recommendation. It is how to make the voice channel itself work for seniors, in both directions. This idea comes from the Sinyi Charity Foundation's Gather Ideas platform.

## Slide 3 — Three objectives, one for each step of a conversation

**Time:** 0:50  |  **Suggested speaker:** Member E  |  **Words:** 112

We set three objectives, and each one matches one step of a conversation.

First, speak naturally. A senior should be able to ask in everyday words, with one big voice button as the main entry. Typing and menus are still available, but only as secondary options, so that new features can be added later.

Second, be understood in noise. Before the recording goes to a speech recognition service, we clean it with our own audio pre-processing.

Third, hear the answer clearly. Before the answer is played, we adjust the synthesized voice for older ears.

The second and third objectives are where we apply what we learned in this course about digital audio.

## Slide 4 — How it works: from microphone to speaker

**Time:** 1:00  |  **Suggested speaker:** Member A  |  **Words:** 169

Here is a typical scenario. Grandma presses the big button and says, "I want to go to the temple." The app recommends a nearby temple and a route with few stairs and places to rest. Everything after her request runs automatically. The app reads the directions aloud as the main guidance, and the route on the screen is a secondary aid. When she arrives, her family can receive a short safe-arrival message.

Below is the system pipeline. The sound from the microphone first goes through our input pre-processing. Then we call an existing speech-to-text API. The app logic finds the intent and recommends a temple and a route. The reply is turned into speech by an existing text-to-speech API, and finally it goes through our output processing before it reaches the speaker.

The two red blocks are what we implement ourselves. The gray blocks are off-the-shelf services. With about six weeks, we do not want to rebuild speech recognition. We want to make existing recognition work better for seniors.

## Slide 5 — Prototype preview: what the senior sees

**Time:** 0:30  |  **Suggested speaker:** Member E  |  **Words:** 62

This short animation is a front-end mockup of the app, with demo data. The senior presses the big voice button and speaks. The app works automatically and reads the recommendation aloud. During the walk, the map shows the current position and the route, with a large turn card and spoken guidance on top. At the end, the family receives a safe-arrival message.

## Slide 6 — Methods 1: Cleaning the voice before recognition

**Time:** 1:30  |  **Suggested speaker:** Member B  |  **Words:** 190

Now the input side. We plan four steps before calling the speech recognition API.

Step one, format conversion. We convert the recording to 16 kilohertz, 16-bit, mono. As we learned from the Nyquist theorem, 16 kilohertz can represent frequencies up to 8 kilohertz, which covers speech and is the usual rate for speech recognition.

Step two, voice activity detection. We split the signal into short frames and compute the energy of each frame in decibels. Frames below a threshold are treated as silence and removed, so the API receives only speech.

Step three, noise reduction, which is the core. We use spectral subtraction. Each frame is multiplied by a Hamming window to reduce spectral leakage, and transformed with the FFT. We estimate the noise spectrum from the silent frames, subtract it from the magnitude, keep the original phase, and go back to the time domain with the inverse FFT and overlap-add.

Step four, level normalization. Seniors often speak softly, so we raise the level to a target in decibels without clipping the 16-bit range.

All four steps use concepts from Unit 4, and we will implement them ourselves in Python.

## Slide 7 — Methods 2: Shaping the reply for older ears

**Time:** 1:10  |  **Suggested speaker:** Member C  |  **Words:** 137

On the output side, the text-to-speech API gives us a clean voice, but it is designed for normal hearing.

Age-related hearing loss mainly affects high frequencies. Those frequencies carry consonants such as s, t and k, so speech sounds loud enough but unclear. Our first step is a hearing compensation equalizer. We transform the signal to the frequency domain, apply more gain roughly between one and four kilohertz, and transform it back. The curve on the right is our starting target. We will tune it after listening tests with seniors.

Second, loudness normalization. Every sentence is adjusted to the same level in decibels, so the guidance is consistently loud outdoors.

Third, we slow down the speaking rate. This is only a parameter of the API, so it is not our own processing, but it matters for seniors.

## Slide 8 — Methods 3: Route recommendation

**Time:** 0:45  |  **Suggested speaker:** Member D  |  **Words:** 103

After recognition, the app turns the text into a recommendation. We keep this part simple.

We extract the intent with keyword rules, with a language model as a backup. Temple data comes from government open data and OpenStreetMap, limited to Minxiong and Xingang in Chiayi. We will add a few labels by hand, such as whether the entrance has stairs and whether there are benches.

Each candidate gets a score: distance and stairs increase the cost, benches reduce it. The weights change with the user's mobility, for example if they use a cane. A safe-arrival message to the family is our stretch goal.

## Slide 9 — Evaluation: does pre-processing help?

**Time:** 0:45  |  **Suggested speaker:** Member C  |  **Words:** 84

How do we know our processing really helps? We will measure it.

We will record twenty to thirty spoken commands in real places, such as a temple courtyard and a roadside. Each recording is sent to the same speech-to-text API twice: once raw, and once after our pre-processing. Then we compare the character error rate of the two results.

We will also show waveforms and spectrograms before and after, and on the output side we will ask a few seniors which voice is clearer.

## Slide 10 — Team responsibilities and six-week plan

**Time:** 0:55  |  **Suggested speaker:** Member A  |  **Words:** 136

Here is how the five of us share the work.

Member A is the project lead and handles the architecture, the backend, and the connection to the speech APIs. Member B builds the input pre-processing: resampling, voice activity detection, noise reduction and normalization. Member C builds the output processing and runs the evaluation experiments. Member D handles the app logic, the temple data and the scoring. Member E designs the big-button interface, leads the field recording and the trials with seniors, and prepares the USR documents.

We have about six weeks. In week one we record test audio and prepare data. In weeks two and three we finish the two audio modules offline. In week four we build the end-to-end prototype, in week five we test on site, and in week six we prepare the demo.

## Slide 11 — Connection to the USR competition

**Time:** 0:55  |  **Suggested speaker:** Member E  |  **Words:** 131

Finally, the connection to the USR competition, whose theme is co-creating a happy life for seniors.

First, social participation. Going to the temple is something seniors already want to do, so we lower the barrier of an existing habit instead of teaching a new one.

Second, digital inclusion. The app is voice-first, so reading and typing are not required, and the audio is adapted to seniors, not the other way around.

Third, local co-creation. Our test recordings and trials come from seniors and temples in Chiayi, so the community helps shape the system.

Fourth, family connection. A safe-arrival message gives family members peace of mind.

In short, we use digital audio techniques from this course to help seniors keep doing something they love. Thank you. We are happy to take questions.
