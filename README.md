# Large Language Models for Mortals: A Practical Guide for Analysts

These are additional materials for my book, *Large Language Models for Mortals: A Practical Guide for Analysts*. Available to purchase in epub or paperback version [from my store](https://crimede-coder.com/store).

![](CoverPage_Print.png)

Any feedback on the book, feel free to leave here on Github, or [message me directly](https://crimede-coder.com/contact).

Andy Wheeler
[Crime De-Coder LLC](https://crimede-coder.com/)
![](/crimepy/CrimeDeCoder_Logo_Small.PNG)

## Environment

I used conda to create the python environment to run the code. To create the environment, I used:

    conda create --name llm_book -c conda-forge python=3.12 gliner sentence-transformers jupyter jupyter-cache anthropic openai boto3 pypdf tiktoken google-genai chromadb docling faiss

Some of these are for the book compilate (jupyter and jupyter cache). Then you need to set up appropriate environment variables for the different models.

....OpenAI, Anthropic, Google Gemini, Bedrock, Claude Code with Bedrock etc.

## Additional Book Materials

You can see the introduction plus the first three chapters here. Some of the code examples in the chapters require additional materials to run. I have placed them here in this repository.

### Chapter 3

These are examples I used as inputs to OpenAI, Google, and Anthropic to show how you can pass in files to interpret.

 - Raleigh search and seizures document, saved as `RaleighSearchSeizure.pdf`, downloaded from <https://public.powerdms.com/RPD1/tree/documents/866204> on 12/5/2025
 - Monthly robberies in Chicago chart, `MonthlyRobberiesChicago.png`, see my crimepy python library for how this was generated, <https://github.com/apwheele/crimepy/blob/main/notebooks/TimeSeriesCharts.ipynb>
 - Audio file, `WebMapAudio11sec.mp3`, first 11 seconds from this Youtube video I made, <https://www.youtube.com/watch?v=mBm6sTR08BI&t=35s>, on describing the cartographic decisions I made around an interactive hotspot map.
 - Audio file, `TrimmedPodcast.mp3`, audio of 95 seconds to 130 seconds from my LEAP podcast with Jason Elder, <https://www.leapodcasts.com/e/atwje-dr-andrew-wheeler-crime-de-coder/>
 - Stata Base Reference Manual (V19), limited to the first 1000 pages, downloaded from <https://www.stata.com/manuals/r.pdf> on 12/13/2025
 - The MP3 video file, `DurhamHotspotClipped.mp4`, is seconds 4:00 to 4:30 of this Youtube video <https://www.youtube.com/watch?v=mBm6sTR08BI> describing a slippy map of Durham hotspots of crime I created


### Chapter 4

I made a test set of cases to show evaluating structured outputs in the `crime_test_data.csv` file. This is entirely made up data.

### Chapter 5

These are examples I used in Chapter 5, RAG. Documents downloaded on 12/7/2025.

 - Raleigh policy documents, via <https://public.powerdms.com/RPD1/tree>
   - 865833.pdf, Use of Force and Weapons
   - 866145.pdf, Interacting with Vulnerable Populations
   - 866181.pdf, Response to Trespassing Complaints
   - 866217.pdf, Taxis and Towing
   - 2208425.pdf, Unmannded Aerial System (UAS) Operations

For the scanned document, I printing out Interacting with Vulnerable Populations (866145.pdf), and then scanned it back in to demonstrate OCR'ing the document.

I also use the Stata reference documentation (see url in Chapter 3), split out with the Table of Contents and the actual document.

### Chapter 6

I use example data from Dallas. You can see the script to download this data from the Dallas open data site at <https://github.com/apwheele/apwheele/blob/main/dallas_data.py>. This data was downloaded in a github action on 12/26/2025 (last date of data on 12/24/2025).

I then used the `prep_dallas_crime.py` script to slightly modify that file (to include column categories instead of the numeric labels, and strip out some data).

The file `crime_mcp.py` is the mcp server script I used in the book with the Claude Desktop tool. You can see my conversation at <https://claude.ai/share/6c14cb84-cdbe-475e-91cd-acf4240f3a60> (unfortunately that does not show the artifacts).

### Chapter 7

The MCP server is a custom one I wrote (with the help of Claude Code) using the [gemimg python library](https://github.com/minimaxir/gemimg), which is a wrapper for Google Gemini image generation models.

`Fig3_KDE_Surveys.png` is from a journal article of mine, [*Mapping Attitudes Towards the Police at Micro Places* (Wheeler et al., 2020)](https://link.springer.com/article/10.1007/s10940-019-09435-8). It is an (anonymized) kernel density map of surveys at different locations.

The sub folder `incident_app` is a Flask app I had Google Antigravity create as an example in the chapter.

This folder also contains `Prompts.txt` with several examples of the longer prompts I wrote in the chapter.


