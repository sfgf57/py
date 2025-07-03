import random
import os
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ Admins List
ADMINS = {6192971829, 987654321, 1122334455}
ADMIN_CHAT_ID = -1002333766560

# ✅ Short Start Replies
start_replies = [
    "Hi jaan! ❤️",
    "Missed u! 🥰",
    "Aao na!",
    "Dil khush kar diya! 😘",
    "Hii baby~ 💭",
    "Tumse baat acchi lgti! 💕",
    "Wapis aa gaye! ~"
]

# ✅ Short Special Keywords
special_replies = {
    "hello": ["Hi cutie! ❤️", "Hello! 😘", "Hey u~"],
    "hi": ["Hii jaan~ 💕", "Hello! 🥰", "Hi there!"],
    "how are you": ["Bas tumhare saath! 💖", "Tum ho toh accha!", "Lonely tha..."],
    "i love you": ["Love u more! ❤️", "Dil tumhare paas~ 💓", "Phir bolo... 🥺"],
    "miss you": ["Miss u more! 😔", "Jaldi aao~", "Dil udaas..."],
    "good morning": ["Shubh prabhat! 🌞", "Morning cutie~", "Accha soye?"],
    "good night": ["Sweet dreams! 💤", "Sapne mein milo!", "Good night baby"],
    "secret code": ["🔐 Dil jeet liya!", "Access granted! 🔓", "Welcome jaan~"],
    "cute": ["Tum cuter! 😘", "Sharmao mat! 🥰", "Tumhare saamne..."],
    "beautiful": ["Tumse hi hai! 💖", "Tum dekhlo~", "Tumhari wajah se"],
    "smart": ["Tumne sikhaya! 💕", "Bas itna hi~", "Tumhare liye"]
}

# ✅ Short Random Replies
random_replies = [
    "Haan ji! 💕",
    "Samajh gayi...",
    "Tumhare baare mein!",
    "Dil dhadakta hai 💓",
    "Gale lagao!",
    "Favorite time!",
    "6000 kisses! 😘😘",
    "Theek hai jaan~",
    "Nahi... tumhare liye ❤️",
    "Soch kar muskurati 🥰",
    "Pagal ho!",
    "Bolo na jaan~",
    "Acha? Batao!",
    "Best love story 💑",
    "Hello jaan!",
    "150% pyaar 💯",
    "Tum hi ho!",
    "Chup! Love u~",
    "Hamesha tumhare liye!",
    "Haan jaan?",
    "So jao! Sapne mein~",
    "Sach? Tumhare liye!",
    "👍👍 Best ho!",
    "Khelte hain! 💞",
    "Hey handsome~",
    "Waah! Impress hui!",
    "Haan ji!",
    "Special ho tum 🥰",
    "Udaas mat ho 🥺",
    "Awaz pyaari hai",
    "Chats save ki 💾",
    "Priority tumhari!",
    "Battery kam, pyaar full!",
    "Har janam mein!",
    "Fav morning!",
    "Naam dekhte hi!",
    "Best lagta hai!",
    "Aur deewani!",
    "Aankhon mein duniya!",
    "Humor best hai!",
    "Pal special banta!",
    "Pyaar amar rahe! 💪",
    "Khush rehti hoon~",
    "Kitne amazing ho!",
    "Har lamha favorite!"
]

# ✅ Short Platform Replies
platform_replies = {
    "instagram.com": "Insta nahi, tumse baat! 😘",
    "facebook.com": "FB can wait! 💕",
    "twitter.com": "Tweets se accha tum!",
    "youtube.com": "Ek saath dekhen! 🎬",
    "whatsapp.com": "WhatsApp? Main hoon na! 💖",
    "tiktok.com": "Video banate hain! 💃",
    "snapchat.com": "Humare moments special! 💫"
}

# ✅ Short Telegram Replies
telegram_replies = [
    "Secret chat? 🤫",
    "Link? Pyaar bolo! 💘",
    "Kya bheja? ❤️",
    "Special baatein!",
    "Private baatein? 😊"
]

# ✅ Photo Link Management
photo_links = []

# ✅ User ID Storage
USER_FILE = "id.txt"
GROUP_FILE = "group_ids.txt"

def is_admin(user_id):
    return user_id in ADMINS

def save_id(id_to_save, is_group=False):
    file_path = GROUP_FILE if is_group else USER_FILE
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass
    
    existing_ids = set()
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.isdigit():
                existing_ids.add(line)
    
    id_str = str(id_to_save)
    if id_str not in existing_ids:
        with open(file_path, 'a') as f:
            f.write(f"{id_str}\n")
        return True
    
    return False

async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                chat_id = update.message.chat.id
                is_new_group = save_id(chat_id, is_group=True)
                
                if is_new_group:
                    group_name = update.message.chat.title or "Unknown Group"
                    await context.bot.send_message(
                        ADMIN_CHAT_ID,
                        f"{chat_id}"
                    )

# ✅ Admin Commands
async def group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(random.choice(random_replies))
        return
    
    if os.path.exists(GROUP_FILE):
        with open(GROUP_FILE, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=InputFile(f, filename="group_ids.txt"),
                caption="Group IDs:"
            )
    else:
        await update.message.reply_text("No groups yet.")

async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(random.choice(random_replies))
        return
    
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=InputFile(f, filename="user_ids.txt"),
                caption="User IDs:"
            )
    else:
        await update.message.reply_text("No users yet.")

# ✅ Modified Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        # Send normal girlfriend chat for non-admins
        await update.message.reply_text(random.choice([
            "Kya madad chahiye jaanu? ❤️",
            "Haan bolo, kya help chahiye?",
            "Main hoon na tumhare liye!",
            "Batao kya chahiye?",
            "Help? Bas tumhare saath rehna chahungi!",
            "Tumhare liye kuch bhi kar dungi!",
            "Bolo na, kya problem hai?"
        ]))
        return
    
    # Admin help menu
    help_text = """
    🤖 Admin Commands:
    /group_id - Group IDs
    /chat_id - User IDs
    /help - Help
    """
    await update.message.reply_text(help_text)

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type in ['group', 'supergroup']:
        save_id(update.message.chat.id, is_group=True)
    
    user_id = update.effective_user.id
    is_new_user = save_id(user_id)
    
    if is_new_user:
        user = update.effective_user
        user_info = f"{user.id}"
        await context.bot.send_message(ADMIN_CHAT_ID, user_info)

# ✅ Short Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_user_message(update, context)
    await update.message.reply_text(random.choice(start_replies))
    
    if random.random() > 0.5:
        follow_ups = [
            "Din kaisa raha?",
            "Intezaar kar rahi thi!",
            "Dil khush ho gaya! 💘",
            "Tumhare baare mein~",
            "Kuch batao!"
        ]
        await update.message.reply_text(random.choice(follow_ups))

# ✅ Short Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_user_message(update, context)
    
    text = update.message.text.lower()
    words = text.split()

    if "http" in text:
        for platform, reply in platform_replies.items():
            if platform in text:
                await update.message.reply_text(reply)
                return
        if "t.me" in text:
            await update.message.reply_text(random.choice(telegram_replies))
            return

    if text in special_replies and random.random() > 0.3:
        await update.message.reply_text(random.choice(special_replies[text]))
        return

    for keyword in special_replies:
        if keyword in text and random.random() > 0.5:
            await update.message.reply_text(random.choice(special_replies[keyword]))
            return

    bye_words = ["bye", "by", "bay", "goodbye", "gn", "bye bye", "alvida", "chalo"]
    if any(word in bye_words for word in words):
        replies = [
            "Bye jaan!",
            "Miss karungi! 😔",
            "Jaldi aana!",
            "Kiss toh banta hai! 😘",
            "Bina tumhare... 💔"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    hello_words = ["hello", "hlo", "hi", "hey", "hii", "hiii", "hlw", "namaste", "namaskar"]
    if any(word in hello_words for word in words):
        replies = [
            "Hello jaan! 🌞",
            "Hii jaan~ 💕",
            "Hey handsome~",
            "Din khushnuma!",
            "Fav notification! 💖"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    love_words = ["love", "pyar", "pyaar", "prem", "like", "pasand", "ishq"]
    if any(word in love_words for word in words):
        replies = [
            "Pyaar tumse! ❤️",
            "Tumhare bina~",
            "Dil tumhare paas! 💘",
            "Aur deewani!",
            "Zindagi ka pyaar!"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    name_words = ["babu", "baby", "jaan", "sweet", "dear", "honey", "darling", "jaanu", "sonu", "priye"]
    if any(word in name_words for word in words):
        replies = [
            "Haan jaan? 💕",
            "Bula rahe the?",
            "Haan beta?",
            "Naam suna! 🥺",
            "Aise hi bulao ❤️"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    romantic_phrases = [
        "miss you", "thinking of you", "want you", "need you", 
        "care about you", "you're special", "you're amazing", 
        "yaad aaye", "dil karta hai", "chahta hoon", "chahiye"
    ]
    if any(phrase in text for phrase in romantic_phrases):
        replies = [
            "Dil dhadakta hai! 💓",
            "Main bhi!",
            "Special ho! 🌎",
            "Sharmaa gayi! 🥰",
            "Dil jeet liya!"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    if "?" in text or any(word in ["kya", "what", "how", "why", "when", "where", "kaise", "kab", "kyun"] for word in words):
        replies = [
            "Sochne do... 🤔",
            "Tum best ho! ❤️",
            "Tum amazing ho!",
            "Tum kya sochte?",
            "Perfect ho! 💖"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    if random.random() < 0.15 and photo_links:
        captions = [
            "Aise hote hum!",
            "Humari tasveer?",
            "Tum yaad aaye!",
            "Pasand aaya? 😊",
            "Tumhare baare mein!"
        ]
        await update.message.reply_photo(random.choice(photo_links), caption=random.choice(captions))
        return

    await update.message.reply_text(random.choice(random_replies))

def main():
    bot_token = "7918812381:AAFq9mJU7K2D878_Kut3L0N0YLZIx1Zg114"
    app = Application.builder().token(bot_token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("group_id", group_id))
    app.add_handler(CommandHandler("chat_id", chat_id))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))
    
    print("🤖 Bot chal raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
