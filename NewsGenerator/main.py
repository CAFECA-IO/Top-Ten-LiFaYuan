from scripts.generate_news_script import generate_news_script
from scripts.generate_storyboard_images import generate_storyboard_images
from scripts.generate_anchor_image import generate_anchor_image
from scripts.generate_animation import generate_animation_from_images
# from scripts.generate_anchor_animation import generate_anchor_animation
# from scripts.generate_voiceover import generate_voiceover
# from scripts.generate_background_music import generate_background_music
# from scripts.combine_media import combine_media

def create_news_broadcast(summary):
    script_path = generate_news_script(summary)
    if not script_path:
        return

    image_paths = generate_storyboard_images(script_path)
    if not image_paths:
        return

    anchor_image_paths = generate_anchor_image(summary)
    if not anchor_image_paths:
        return

    # 使用 generate_animation_from_images 來生成整個新聞播報的動畫，基於分鏡稿圖片生成動畫片段。
    animation_paths = generate_animation_from_images(image_paths)
    if not animation_paths:
        return

    # voiceover_path = generate_voiceover(script_path)
    # if not voiceover_path:
    #     return

    # background_music_path = generate_background_music(script_path)
    # if not background_music_path:
    #     return

    # # 使用 generate_anchor_animation 來生成基於主播圖片和語音的動畫，這樣動畫的重點將是主播與新聞講稿的同步呈現。
    # anchor_animation_path = generate_anchor_animation(anchor_image_paths, voiceover_path)
    # if not anchor_animation_path:
    #     return

    # # 有兩種視頻片段可以進行合成 animations 和 anchor_animation 
    # combine_media(anchor_animation_path, voiceover_path, background_music_path)

# 示例使用：使用生成的逐字稿摘要來創建新聞播報
if __name__ == "__main__":
    summary = """
    1. 使用者向總統和相關部門官員提出關於 Peer-to-Peer(P2P) 監管問題的擔憂，尤其是在缺乏法律約束和自我監管下的非法活動。
    2. 官員承認在目前的法律框架下，對於 P2P 平臺的管理存在困難，但強調正在研究各種選項，包括成立行業協會和逐步實施分級管理。
    3. 用戶表達了對政府在面對金融科技快速發展時，是否具備明確的戰略和行動計劃的疑慮。
    4. 金融監督管理委員會（FSC）表示，他們正在努力平衡創新和風險管理，同時呼籲企業遵守相關法律法規。
    5. 會上還提及了房地產市場泡沫和銀行信貸比例過高的問題，官方承諾將與中央銀行協調，採取相應措施防止金融危機。
    6. 與會者同意進一步研究並追蹤相關議題，以促進金融業的健康發展。
    """

    create_news_broadcast(summary)
