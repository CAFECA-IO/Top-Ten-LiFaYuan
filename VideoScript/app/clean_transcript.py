import os
import spacy
from transformers import pipeline
import re

# 加載 Spacy 中文模型
nlp = spacy.load("zh_core_web_sm")

# 加載 Hugging Face 的預訓練模型進行錯別字修正
corrector = pipeline('fill-mask', model='bert-base-chinese')

# 修正錯別字和專有名詞的字典
corrections = {
    "主席副院長": "主席、副院長",
    "郵請": "請",
    "總市長": "董事長",
    "低探": "低碳",
    "探排電": "碳排放",
    "戰比": "占比",
    "站比": "占比",
    "經典": "經濟",
    "戰生人員": "再生能源",
    "站生人員": "再生能源",
    "立向": "比例",
    "馬雙": "馬上",
    "共企": "公頃",
    "要MAGAW": "要增加",
    "郭高楊": "郭高雄",
    "政協議次長": "政務次長",
    "陳政協": "陳正祺",
    "同志嫌": "童子賢",
    "同總市長": "童董事長",
    "低探發電": "低碳發電",
    "政界": "政見",
    "內心的總統": "賴清德總統",
    "戰生能源": "再生能源",
    "站生能源": "再生能源",
    "不死文件": "不實文件",
    "立向": "比例",
    "探排電": "碳排放",
    "戰時點期盤": "占時點期盤",
    "電戰比": "電占比",
    "政協次長": "政務次長",
    "院長": "行政院院長",
    "開支票": "承諾",
    "立揚": "立陽",
    "私政": "施政",
    "藍氣": "燃氣",
    "經典打算": "經濟部打算",
    "劉書瑋": "劉書偉",
    "郭高楊": "郭高雄",
    "來捷務": "來自捷運",
    "陳政祺": "陳政祺",
    "李潔文": "李潔雯",
    "哇斯轉男女青": "瓦斯轉燃氣",
    "白皮書": "白皮書",
    "基於什麼樣子的原因": "基於什麼原因",
    "元政策": "能源政策",
    "入境": "路徑",
    "變遷的委員會": "變遷委員會",
    "批評我知道同總市長": "批評。我知道童董事長",
    "非常有社會企業社會責任感": "非常有社會責任感",
    "百分之百去剪掉": "百分之百去減掉",
    "第一探發電比例": "低碳發電比例",
    "把火力發電然沒跟藍氣加在一起": "把火力發電和燃氣加在一起",
    "就是把火力發電然沒跟藍氣加在一起用百分之百去剪掉我們火力發電的數字": "就是把火力發電和燃氣加在一起，用百分之百去減掉我們火力發電的數字",
    "經濟部能源數": "經濟部能源數據",
    "左院長": "行政院院長",
    "我喜歡討論事情從事實開始因為這樣子的發言事實上是代表了我們在建立太盤的道路上面不進反退我們就先從事實開始同總市長這樣子的數據剛剛對不起您是委員經濟部次長陳政協議次長說你不知道正不正確你還要再回去再確認是嗎是好來我跟市長報告他的數據是正確的": "我喜歡討論事情從事實開始。因為這樣子的發言事實上是代表了我們在建立太陽能的道路上面不進反退。我們就先從事實開始。童董事長這樣子的數據，剛剛對不起，您是委員。經濟部次長陳正祺說你不知道正不正確，你還要再回去再確認，是嗎？好，來，我跟市長報告，他的數據是正確的。",
    "2015戰生人員要打到20%七年的經濟部也承認了這是一個沒有辦法打到的政界確定跳票的內心的總統也很坦率的承認了這件事情做不到啦做不到他接棒下去做要2026年才可以實踐": "2015年再生能源要達到20%。七年的經濟部也承認了這是一個沒有辦法達到的政見，確定跳票。賴清德總統也很坦率地承認了這件事情做不到。做不到，他接棒下去，要到2026年才可以實踐。",
    "發展戰生人員": "發展再生能源",
    "戰生人員發電量": "再生能源發電量",
    "10.7%我們2026年要到20%": "10.7%，我們2026年要到20%",
    "我具體的請教你們到2026年要達成20%的戰生人員的入境當中太陽光電你們估計要達到20%太陽光電要戰幾%": "我具體請教你們，到2026年要達成20%的再生能源的路徑當中，太陽光電你們估計要達到多少？太陽光電要占比多少？",
    "你們現在有幾個火力發電想要停下來": "你們現在有幾個火力發電機組想要停下來",
    "我知道再生能源很多所以我把所有的數字都列出來了這個是經濟不能源屬的網站公告的嘛我今天要問題很簡單愛心的總統開了政見我們大家都願意相信他他要努力的去達成政見達成要有入境剛剛院長你也表示同意嘛現在再生能源20%2026年要到20%其中太陽光電你們目前的施政計劃是戰幾%這個問題很具體一點都不複雜也不困難太陽光電要戰幾%": "我知道再生能源很多，所以我把所有的數字都列出來了，這是經濟部能源署的網站公告的。我今天問題很簡單，賴清德總統開了政見，我們大家都願意相信他，他要努力去達成政見。達成要有路徑。剛剛院長你也表示同意嘛，現在再生能源20%，2026年要到20%。其中，太陽光電你們目前的施政計劃是占多少？這個問題很具體，一點都不複雜也不困難。太陽光電要占多少？"
}

def correct_text(text):
    """
    使用字典和上下文模型修正文本中的錯別字和專有名詞。
    """
    # 使用字典進行初步修正
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)

    # 使用 BERT 模型進行上下文感知的修正
    tokens = text.split()
    for i, token in enumerate(tokens):
        if '[MASK]' in token:
            masked_text = text.replace(token, '[MASK]')
            predictions = corrector(masked_text)
            tokens[i] = predictions[0]['token_str']
    corrected_text = ' '.join(tokens)
    
    return corrected_text

def clean_transcript(transcript):
    """
    清理逐字稿文本，包括修正錯別字和專有名詞，添加標點符號等。
    """
    transcript = correct_text(transcript)

    # 使用 Spacy 進行分詞和命名實體識別
    doc = nlp(transcript)

    # 添加標點符號
    transcript = re.sub(r"([。！？])", r"\1\n", transcript)  # 將句號、驚嘆號和問號後添加換行符
    transcript = re.sub(r"([，])", r"\1 ", transcript)  # 在逗號後添加空格

    return transcript

if __name__ == "__main__":
    # 示例逐字稿文件
    video_id = "154397"  # 假設這是視頻的ID
    version = "v2"
    transcript_filename = f'meeting_script_{video_id}_{version}.txt'
    transcript_path = os.path.join('scripts', transcript_filename)

    # 讀取逐字稿文本
    with open(transcript_path, 'r', encoding='utf-8') as file:
        example_transcript = file.read()

    # 清理逐字稿文本
    cleaned_transcript = clean_transcript(example_transcript)

    # 儲存清理後的逐字稿
    cleaned_transcript_filename = f'cleaned_meeting_script_{video_id}.txt'
    cleaned_transcript_path = os.path.join('scripts', cleaned_transcript_filename)

    with open(cleaned_transcript_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_transcript)

    print(f"清理後的逐字稿已儲存至：{cleaned_transcript_path}")
