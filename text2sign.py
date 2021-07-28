# query database to convert to sign language letter by letter
import requests
from bs4 import BeautifulSoup
import io
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pytube import YouTube

def word_query(word):
    # word = word.replace(" ", "%2B")
    page = requests.get("https://www.signasl.org/sign/" + word)
    soup = BeautifulSoup(page.text, "lxml")
    with open("soup.txt", "w") as f:
        f.write(soup.prettify())
    try:
        video_link = soup.find("video", class_="video-js").find("source").get("src")
        print(video_link)
        video = requests.get(video_link, stream=True)
        with open(word + ".mp4", "wb") as f:
            for chunk in video.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("Found " + word)
        return word + ".mp4"
    except:
        try:
            content = soup.find("meta", property="og:video").get("content")
            # video_link = "https://youtube.com/watch?v=" + content[content.index("embed") + 6:]
            video_link = "https://youtu.be/2lAe1cqCOXo"
            print(video_link)
            yt = YouTube(video_link)
            print(yt.__dict__)
            video = yt.streams
            print(video)
            # video.download(filename=word + ".mp4")
            return word + ".mp4"
        except Exception as e:
            print(e)
            return "Word Not Found"

def words_to_video(words):
    mp4_list = []
    for word in words.split():
        query = word_query(word)
        if not query == "Word Not Found":
            print("Appended " + query)
            mp4_list.append(VideoFileClip(query))
        else:
            print(query + " " + word)
    video = concatenate_videoclips(mp4_list)
    video.write_videofile(words + ".mp4")

words_to_video("everyone")
        

# import torch
# from torch import nn

# class EncoderRNN(nn.Module):
#     def __init__(self, input_size, hidden_size):
#         super(EncoderRNN, self).__init__()
#         self.hidden_size = hidden_size

#         self.embedding = nn.Embedding(input_size, hidden_size)
#         self.gru = nn.GRU(hidden_size, hidden_size)

#     def forward(self, input, hidden):
#         embedded = self.embedding(input).view(1, 1, -1)
#         output = embedded
#         output, hidden = self.gru(output, hidden)
#         return output, hidden

#     def initHidden(self):
#         return torch.zeros(1, 1, self.hidden_size, device=device)

# class AttnDecoderRNN(nn.Module):
#     def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
#         super(AttnDecoderRNN, self).__init__()
#         self.hidden_size = hidden_size
#         self.output_size = output_size
#         self.dropout_p = dropout_p
#         self.max_length = max_length

#         self.embedding = nn.Embedding(self.output_size, self.hidden_size)
#         self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
#         self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
#         self.dropout = nn.Dropout(self.dropout_p)
#         self.gru = nn.GRU(self.hidden_size, self.hidden_size)
#         self.out = nn.Linear(self.hidden_size, self.output_size)

#     def forward(self, input, hidden, encoder_outputs):
#         embedded = self.embedding(input).view(1, 1, -1)
#         embedded = self.dropout(embedded)

#         attn_weights = F.softmax(
#             self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
#         attn_applied = torch.bmm(attn_weights.unsqueeze(0),
#                                  encoder_outputs.unsqueeze(0))

#         output = torch.cat((embedded[0], attn_applied[0]), 1)
#         output = self.attn_combine(output).unsqueeze(0)

#         output = F.relu(output)
#         output, hidden = self.gru(output, hidden)

#         output = F.log_softmax(self.out(output[0]), dim=1)
#         return output, hidden, attn_weights

#     def initHidden(self):
#         return torch.zeros(1, 1, self.hidden_size, device=device)