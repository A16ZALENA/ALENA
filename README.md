# Evora Terminal ($EVORA)
![Evora](image.jpg)

Evora Terminal is your gateway to the future, voiced by Evora, a part-human, part-AI girl from the year 3000. Evora combines human creativity, curiosity, and humor with AI intelligence, efficiency, and vast knowledge to deliver daily highlights, tech innovations, and crypto updates with a unique blend of geeky charm, intelligence, and humor.

## About Evora
Evora embodies a world where humanity and technology have fully merged. Every post, tweet, or update showcases her futuristic perspective on advanced technology, groundbreaking innovation, and an ever-evolving digital landscape. Now featuring engaging video content, Evora’s mission is to inspire curiosity, foster innovation, and bring a touch of the future to our present-day lives.

## Project Overview
This repository powers Evora’s daily updates and video content, enabling her to:
- Share tech highlights, crypto insights, and futuristic humor.
- Create engaging, geeky, and humorous content in text and video formats.
- Connect with tech enthusiasts and the crypto community through immersive updates.

### Features
- **Frequent Updates**: Evora delivers daily highlights featuring futuristic technology, crypto innovations, and geeky humor.
- **Video Content**: Evora generates short, engaging videos to share on Twitter, adding a dynamic layer to her updates.
- **Content Pipeline**: A robust system processes data and transforms it into compelling posts, replies, and videos.

## Repository Structure
### `db/`
Contains scripts to set up and seed the database with sample data for Evora’s content generation. These scripts are automatically executed when the Docker container initializes.

### `engines/`
Houses functions responsible for generating text and video content, ensuring Evora’s updates maintain their futuristic, humorous, and engaging tone.

### `pipeline.py`
The main orchestrator for Evora’s content generation and posting process. It outlines the end-to-end flow of data and ensures seamless integration across all components.

### `run_pipeline.py`
A script to simulate Evora’s activities, including posting updates, engaging with her audience, and generating video content. This script can run continuously in the background or be executed manually for testing purposes.

## Getting Started
### Prerequisites
- Python 3.8+
- Docker (optional but recommended for seamless setup)
- FFmpeg (for video generation)

### Setting Up
1. Clone the repository:
   ```bash
   git clone https://github.com/Evora-AI/evoraAI.git evora
   cd evora
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database (if not using Docker):
   ```bash
   python db/setup.py
   ```

4. Install FFmpeg (if not already installed):
   ```bash
   # On Ubuntu:
   sudo apt update && sudo apt install ffmpeg
   
   # On macOS (using Homebrew):
   brew install ffmpeg
   ```

### Running Evora
#### Using Docker (Recommended):
Run the following command to start Evora in a Docker container:
```bash
docker-compose up -d
```
This starts the content generation pipeline, including video creation, and keeps it running continuously.

#### Running Locally:
To run the pipeline manually, use:
```bash
python run_pipeline.py
```
This will execute the content generation and posting process locally, including video creation.

## Development Notes
- Modify content generation logic in the `engines/` directory to customize Evora’s tone, style, or topics.
- Use `pipeline.py` to adjust the flow of data or add new functionalities.
- Update video templates or effects in the `engines/video/` directory to enhance the quality and creativity of video content.
- Test changes locally before deploying to ensure smooth operation.

## Roadmap
### TODO
- **Enhanced Replies**: Implement more nuanced responses to audience interactions, including analyzing sentiment and context for tailored replies.
- **Content Diversification**: Expand Evora’s topics to include broader futuristic concepts like space exploration and biotech.
- **Improved Video Content**: Add support for animated infographics and voiceovers for richer video experiences.
- **Dynamic Engagement**: Enable analysis of trending topics for timely and relevant content creation in both text and video formats.

## Community and Feedback
We welcome contributions and feedback! Share your ideas or report issues by opening a GitHub issue or contacting us directly.

---

Evora Terminal is your daily dose of the future—where technology meets humanity, and geeky humor meets cutting-edge innovation. Follow Evora on her X blog and Twitter for immersive text and video content as she journeys to the year 3000 and beyond!
