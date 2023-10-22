# Image Scraper for ________ (in my case, a music shop)

## Introduction

A local music store recently held a little event to find a hidden picture throughout their website. The award was about $100.

So I made this little script that will compare images through the entire website and do the searching for me.

It does a good job getting most of the images and storing them all locally into a folder in your computer.

### Why I made this

1. **Research & Analysis**: By having an offline collection of the images, I can easily categorize and analyze where the hidden image is located by looking at the descriptive file name. You can also do your own research for a specific thing you want.
   
2. **Visual Search**: The tool's ability to match images to a reference allows me to identify similar products or branding, which can be incredibly useful when looking for products of a specific design or style.
   
3. **Automation**: Automating this process saves countless hours that would otherwise be spent manually downloading and categorizing images.

## How It Works

1. **URL Initiation**: The script starts with a base URL.

2. **Reference Image Matching**: An 'image hash' of a reference image is computed. As the script downloads images, it compares each one to this hash to identify visual similarities.

3. **Recursive Scraping**: The scraper doesn't just download images from the initial page; it also follows links and continues the process, ensuring a comprehensive scrape.

4. **Intelligent File Naming**: Images are saved with names that provide context about their origin, ensuring they can be traced back to their source pages if needed.

5. **Original File Extensions**: The scraper retains the original file extensions (be it `.jpg`, `.png`, `.gif`, etc.), ensuring that the integrity of the images is maintained.

## Usage

Ensure you have the required libraries installed:

```bash
pip3 install requests beautifulsoup4 Pillow imagehash
```

Then, simply run the script:
```bash
python3 scraper_script.py
```

The images will be downloaded into a folder named `downloaded-img`.

Conclusion
This tool was created out of a need to efficiently gather and analyze visual data from any website. It's a testament to how automation can aid research and personal projects. Whether you're a developer, a musician, or just someone curious about web scraping, I hope you find this tool insightful and useful!
