import pandas as pd
import re
import emoji
import matplotlib.pyplot as plt

def startsWithDateTime(s):
    pattern = '^(\[)(([1-9])|(1)[0-2])(\/)([1-9]|[1-2][0-9]|(3)[0-1])(\/)(\d{2}|\d{4}), ([1-9]|(1)[0-2]):[0-6][0-9]:[0-6][0-9] [A-Z][A-Z](\])'
    result = re.match(pattern, s)
    if result:
        return True
    return False
    
def startsWithAuthor(s):
    patterns = [
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
        '([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
        '([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False
    
conversationPath = ''#Enter path to the file which needs to be analyzed
df=pd.DataFrame(columns=['Date','Time','Author','Message'])
with open(conversationPath, encoding="utf-8") as fp:
    fp.readline() # Skipping first line of the file (usually contains information about end-to-end encryption)
    while True:
        line = fp.readline() 
        if not line:
            break
        line = line.strip() 
        if startsWithDateTime(line):
            splitLine = line.split('] ')
            dateTime = splitLine[0] 
            date, time = dateTime.split(', ') 
            message = ' '.join(splitLine[1:])  
            if startsWithAuthor(message): 
                splitMessage = message.split(': ')
                author = splitMessage[0] 
                message = ' '.join(splitMessage[1:]) 
            else:
                author = None
            data=[date, time, author, message]
    #print(data)
            a_series = pd.Series(data, index = df.columns)
            df = df.append(a_series, ignore_index=True)
        else:
            message=message+' '+line
df['Date']=df['Date'].str.replace('[','')

# no of messages
author_value_counts = df['Author'].value_counts()
author_value_counts

df['Letter_Count'] = df['Message'].apply(lambda s : len(s))
df['Word_Count'] = df['Message'].apply(lambda s : len(s.split(' ')))

#time series monthly
df['Date']=pd.to_datetime(df['Date'], format='%m/%d/%y')
df['Time']=pd.to_datetime(df['Time'], format='%I:%M:%S %p')
df=df[~df['Author'].isnull()]
x=df[~df['Author'].isnull()].groupby(['Date']).count().reset_index()['Date'].tolist()
y=df[~df['Author'].isnull()].groupby(['Date']).count().reset_index()['Message'].tolist()
a=df.set_index(df['Date'])
a['Date'].resample('M', how='count').plot.line()

#timeseries daily
plt.plot(x,y)
#plt.title('title name')
plt.xlabel('Date')
plt.ylabel('# of messages')
plt.xticks(rotation=45)
#for xy in zip(x, y):                                       # <--
#    plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') # <--
plt.show()

stopwords = ['', ' ','a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

#word freq
author=df['Author'].unique()
wf=pd.DataFrame(columns=['Author','Word','Freq'])
for a in author:
    inter=df[df['Author']==a]
    string=inter['Message'].str.cat(sep=' ').lower()
    string = re.sub('[^a-zA-Z0-9 \n]', '', string)
    wordlist=string.split(' ')
    #print(wordlist)
    l=[]
    for word in wordlist:
        if ((word not in stopwords) and (len(word)>3)):
            freq=string.count(word)
            lst=[word,freq]
            l.append(lst)
    import itertools
    l.sort()
    l=list(l for l,_ in itertools.groupby(l))
    wf1=pd.DataFrame(l,columns=['Word','Freq'])
    #a_series = pd.Series(l, index = wf1.columns)
    #wf1 = wf1.append(a_series, ignore_index=True)
    wf1['Author']=a
    wf=wf.append(wf1)
for a in author:
    a=wf[wf['Author']==a].sort_values(by='Freq' ,ascending=False)
    a=a.reset_index(drop=True)
    try:
        print('Most frequently used word by '+ a['Author'][0] + ' is "' +a['Word'][0] + '" with frequency '+str(a['Freq'][0] ))
    except IndexError:
        continue
        
# import emoji module  
#frquently used emoji
import emoji 
  
def get_emoji(s):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return re.findall(emoji_pattern,s)

def has_emoji(s):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return bool(re.search(emoji_pattern,s))

mask=[]
for i in range(len(df)):
    mask.append(has_emoji(df.iloc[i]['Message']))
emo=df[mask]
emoticon=[]
for i in range(len(emo)):
    emoticon.append(get_emoji(emo.iloc[i]['Message']))
emo['emoticon']=emoticon

author=emo['Author'].unique()
for a in author:
    st=emoji.demojize(emo[emo['Author']==a]['emoticon'].to_string()).replace('[:','').replace(':]','').replace('::',' ').replace(',','')
    wordlist = st.split()
    wordfreq = []
    for w in wordlist:
        wordfreq.append(wordlist.count(w))
    l=list(zip(wordfreq,wordlist))
    l.sort(reverse=True)
    import itertools
    l=list(l for l,_ in itertools.groupby(l))
    emoji.emojize(':'+l[0][1]+':')
    print(a+' used ' + emoji.emojize(':'+l[0][1]+':')+' emoji '+str(l[0][0])+' times')
  
#who initiated the conversation
df['rank'] = df.groupby(['Date'])['Time'].rank()
a=df[df['rank']==1].groupby('Author').count().reset_index()
for i in range(len(a)):
    print('# of times '+a.iloc[i]['Author'] +' started conversation is '+ str(a.iloc[i]['rank']))
    
#who is more verbose
df.groupby('Author')['Word_Count'].mean()
