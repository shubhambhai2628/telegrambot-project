import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Constants
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    logging.warning("GEMINI_API_KEY not found. AI features will be disabled.")
    model = None

# Flask App for Keep-Alive
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run_http():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run_http)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    welcome_text = (
        f"Hi {user}! 👋\n\n"
        "I'm Shubham's Smart Resume Bot. I can help you learn more about him.\n"
        "I am also powered by **Google Gemini**! Ask me any coding question.\n"
        "Please choose an option below:"
    )
    
    keyboard = [
        [KeyboardButton("📧 Contact Info"), KeyboardButton("👨‍💻 Skills")],
        [KeyboardButton("💻 Coding Sources"), KeyboardButton("📚 Courses")],
        [KeyboardButton("ℹ️ About Me"), KeyboardButton("☕ Donate / Hire Me")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_text,
        reply_markup=reply_markup
    )



async def contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📧 **Contact Information**\n\n"
        "• **Email**: shubhamteli2628@gmail.com\n"
        "• **LinkedIn**: [Insert LinkedIn URL]\n"
        "• **GitHub**: c:\\Users\\shubh\\shubham\\resume-bot\\\n"
        "• **Phone**: [Insert Phone Number]"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

async def skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👨‍💻 **Technical Skills**\n\n"
        "• **Languages**: Python, JavaScript, C++, HTML/CSS\n"
        "• **Frameworks**: React, Node.js, Express\n"
        "• **Tools**: Git, Docker, VS Code\n"
        "• **Database**: MongoDB, SQL"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

async def coding_sources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💻 **Coding Language Sources & Docs**\n\n"
        "Official documentation and best references:\n\n"
        "🐍 **Python**: [Official Docs](https://docs.python.org/3/) | [Real Python](https://realpython.com/)\n"
        "🌐 **JavaScript**: [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | [JavaScript.info](https://javascript.info/)\n"
        "🚀 **C++**: [LearnCpp](https://www.learncpp.com/) | [cppreference](https://en.cppreference.com/)\n"
        "☕ **Java**: [Oracle Docs](https://docs.oracle.com/en/java/) | [Baeldung](https://www.baeldung.com/)\n"
        "🎨 **HTML/CSS**: [MDN HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) | [CSS-Tricks](https://css-tricks.com/)\n"
        "🐦 **Flutter/Dart**: [Flutter Docs](https://docs.flutter.dev/)\n"
        "🗺️ **Roadmap**: [Roadmap.sh](https://roadmap.sh/)"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

# --- Course Sub-Menu Handlers ---

async def courses_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for courses. Displays UDEMY by default (Customer Requirement)."""
    text = (
        "🎓 **Udemy & Paid Courses (Recommended)**\n\n"
        "**[Udemy](https://www.udemy.com/)** is the default recommendation for learning specific skills.\n"
        "🔥 **Sale Advice**: Never pay full price! Wait for sales to get courses **under ₹499** ($10).\n\n"
        "**Top Recommendations on Udemy:**\n"
        "1. **Python**: 100 Days of Code (Angela Yu)\n"
        "2. **Web Dev**: The Web Developer Bootcamp (Colt Steele)\n"
        "3. **React**: React - The Complete Guide (Maximilian Schwarzmüller)\n\n"
        "👇 **Other Professional Platforms:**\n"
        "• **Coursera**: For Google/IBM professional certificates.\n"
        "• **EdX**: For Harvard/MIT university courses."
    )
    
    # Sub-menu keyboard
    keyboard = [
        [KeyboardButton("🆓 Free Resources"), KeyboardButton("👶 Beginner Guide")],
        [KeyboardButton("🔙 Back to Main Menu")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text, 
        parse_mode='Markdown', 
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def beginner_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👶 **Absolute Beginner Guide**\n\n"
        "Never coded before? Start here:\n\n"
        "1. **[CS50 by Harvard](https://cs50.harvard.edu/x/)**: The best intro to Computer Science (Free).\n"
        "2. **[Khan Academy](https://www.khanacademy.org/computing/computer-programming)**: Interactive logic building.\n"
        "3. **[Python for Everybody](https://www.py4e.com/)**: Simplest way to learn Python.\n"
        "4. **[Scratch](https://scratch.mit.edu/)**: Visual programming to understand logic."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

async def free_resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🆓 **Free Learning Resources**\n\n"
        "**🌐 Web Development**\n"
        "• [freeCodeCamp](https://www.freecodecamp.org/)\n"
        "• [The Odin Project](https://www.theodinproject.com/)\n\n"
        "**💼 Interview Prep**\n"
        "• [LeetCode](https://leetcode.com/)\n"
        "• [NeetCode](https://neetcode.io/)\n\n"
        "**🤖 AI, Data Science & Analytics**\n"
        "• **Google Data Analytics**: [Coursera](https://www.coursera.org/professional-certificates/google-data-analytics)\n"
        "• **Google Advanced Data Analytics**: [Coursera](https://www.coursera.org/professional-certificates/google-advanced-data-analytics)\n"
        "• **IBM Data Science**: [Coursera](https://www.coursera.org/professional-certificates/ibm-data-science)\n"
        "• **Machine Learning (Andrew Ng)**: [Coursera](https://www.coursera.org/specializations/machine-learning-introduction)\n"
        "• **Deep Learning**: [deeplearning.ai](https://www.deeplearning.ai/)\n"
        "• **Kaggle**: [Kaggle Learn](https://www.kaggle.com/learn)\n"
        "• **Fast.ai**: [Fast.ai (Free)](https://www.fast.ai/)\n\n"
        "**🏗️ System Design**\n"
        "• [System Design Primer](https://github.com/donnemartin/system-design-primer)\n"
        "• [ByteByteGo](https://bytebytego.com/)\n\n"
        "**☁️ DevOps & Cloud**\n"
        "• [DevOps Roadmap](https://roadmap.sh/devops)\n"
        "• [Learn Docker](https://docker-curriculum.com/)"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown', disable_web_page_preview=True)



async def donate_hire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "☕ **Support & Services**\n\n"
        "**Hire Me:**\n"
        "I am available for freelance projects and consulting.\n"
        "📩 Contact me: shubhamteli2628@gmail.com\n\n"
        "**Support the Bot:**\n"
        "If you found this helpful, consider buying me a coffee!\n"
        "💳 **[Buy Me a Coffee](https://www.buymeacoffee.com/)**"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

async def about_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ **About Me**\n\n"
        "I am a passionate developer eager to build impactful solutions. "
        "I love coding, learning new technologies, and solving complex problems."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    
    # Main Menu Handlers
    # Main Menu Handlers
    if msg == "📧 Contact Info":
        await contact_info(update, context)
    elif msg == "👨‍💻 Skills":
        await skills(update, context)
    elif msg == "💻 Coding Sources":
        await coding_sources(update, context)
    elif msg == "📚 Courses":  # New Entry Point
        await courses_menu(update, context)
    elif msg == "☕ Donate / Hire Me":
        await donate_hire(update, context)
    elif msg == "ℹ️ About Me":
        await about_me(update, context)
    
    # Sub-Menu Handlers
    elif msg == "🆓 Free Resources":
        await free_resources(update, context)
    elif msg == "👶 Beginner Guide":
        await beginner_guide(update, context)
    elif msg == "💰 Paid Courses": # If they somehow click this button from old state, route to main
         await courses_menu(update, context)
    elif msg == "🔙 Back to Main Menu":
        await start(update, context) # Re-send main menu
        
    else:
        # Handle random text (Chat capabilities)
        await handle_generic_chat(update, context)

async def handle_generic_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responds to user text with simple keywords or Gemini AI."""
    msg = update.message.text.lower()
    chat_id = update.effective_chat.id
    
    # --- 1. Keyword Overrides (Instant Response) ---
    
    response = None

    if "python" in msg:
        response = (
            "🐍 **Python Resources**\n"
            "Here is the best way to learn Python:\n"
            "• **Course**: [100 Days of Code (Udemy)](https://www.udemy.com/course/100-days-of-code/)\n"
            "• **Free**: [Python for Everybody](https://www.py4e.com/)\n"
            "• **Docs**: [Official Documentation](https://docs.python.org/3/)"
        )
    elif "javascript" in msg or "js" in msg:
        response = (
            "💛 **JavaScript Resources**\n"
            "• **Course**: [The Complete JavaScript Course (Udemy)](https://www.udemy.com/course/the-complete-javascript-course/)\n"
            "• **Free**: [JavaScript.info](https://javascript.info/)\n"
            "• **Docs**: [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)"
        )
    elif "react" in msg:
        response = (
            "⚛️ **React Resources**\n"
            "• **Course**: [React - The Complete Guide (Udemy)](https://www.udemy.com/course/react-the-complete-guide-incl-redux/)\n"
            "• **Free**: [React Official Docs](https://react.dev/learn)\n"
            "• **Practice**: Build a To-Do App first!"
        )
    elif "java" in msg and "script" not in msg: # Avoid matching javascript
        response = (
            "☕ **Java Resources**\n"
            "• **Course**: [Java Programming Masterclass (Udemy)](https://www.udemy.com/course/java-the-complete-java-developer-course/)\n"
            "• **Free**: [Mooc.fi (University of Helsinki)](https://java-programming.mooc.fi/)"
        )
    elif "c++" in msg or "cpp" in msg:
        response = (
            "🚀 **C++ Resources**\n"
            "• **Learn**: [LearnCpp.com](https://www.learncpp.com/) (Best text-based resource)\n"
            "• **Reference**: [cppreference.com](https://en.cppreference.com/w/)"
        )
    elif "html" in msg or "css" in msg or "web" in msg:
        response = (
            "🌐 **Web Development Resources**\n"
            "• **Start Here**: [The Odin Project](https://www.theodinproject.com/)\n"
            "• **Video**: [FreeCodeCamp on YouTube](https://www.youtube.com/c/Freecodecamp)"
        )
    elif "data" in msg or "ai" in msg or "ml" in msg or "analytics" in msg or "science" in msg:
         response = (
            "🤖 **Data Science, Analytics & AI Resources**\n\n"
            "Here is the complete list for Data & AI:\n\n"
            "**🎓 Professional Certificates (Coursera)**\n"
            "• **[Google Data Analytics](https://www.coursera.org/professional-certificates/google-data-analytics)** (Beginner)\n"
            "• **[Google Advanced Data Analytics](https://www.coursera.org/professional-certificates/google-advanced-data-analytics)** (Python-focused)\n"
            "• **[IBM Data Science](https://www.coursera.org/professional-certificates/ibm-data-science)**\n"
            "• **[Google IT Automation with Python](https://www.coursera.org/professional-certificates/google-it-automation)**\n\n"
            "**🧠 Machine Learning & AI**\n"
            "• **[Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction)** (Andrew Ng)\n"
            "• **[Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning)**\n"
            "• **[Fast.ai](https://www.fast.ai/)** (Best Logic-First Approach)\n"
            "• **[Kaggle](https://www.kaggle.com/learn)** (Free Micro-Courses)\n\n"
            "**math**: [Khan Academy Linear Algebra](https://www.khanacademy.org/math/linear-algebra)"
        )
    elif "system design" in msg or "scalability" in msg or "architecture" in msg:
        response = (
            "🏗️ **System Design Resources**\n"
            "• **Read**: [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)\n"
            "• **Watch**: [Gaurav Sen on YouTube](https://www.youtube.com/c/GauravSensei)\n"
            "• **Practice**: [ByteByteGo](https://bytebytego.com/)"
        )
    elif "devops" in msg or "cloud" in msg or "docker" in msg or "kubernetes" in msg:
        response = (
            "☁️ **DevOps & Cloud**\n"
            "• **Roadmap**: [DevOps Roadmap](https://roadmap.sh/devops)\n"
            "• **Learn Docker**: [Docker Curriculum](https://docker-curriculum.com/)\n"
            "• **AWS**: [AWS Free Tier](https://aws.amazon.com/free/)"
        )

    elif "node" in msg or "express" in msg:
        response = (
            "🟢 **Node.js & Express Resources**\n"
            "• **Course**: [NodeJS - The Complete Guide (Udemy)](https://www.udemy.com/course/nodejs-the-complete-guide/)\n"
            "• **Free**: [The Odin Project (Node)](https://www.theodinproject.com/paths/full-stack-javascript/courses/nodejs)\n"
            "• **Docs**: [Node.js Docs](https://nodejs.org/en/docs/)"
        )

    elif "sql" in msg or "database" in msg or "mongodb" in msg:
        response = (
            "🗄️ **Database Resources (SQL & NoSQL)**\n"
            "• **Course**: [SQL - The Complete Developer's Guide (Udemy)](https://www.udemy.com/course/sql-and-postgresql/)\n"
            "• **Free**: [W3Schools SQL](https://www.w3schools.com/sql/)\n"
            "• **Practice**: [SQLZoo](https://sqlzoo.net/)"
        )

    elif "git" in msg or "github" in msg:
        response = (
            "🐙 **Git & GitHub Resources**\n"
            "• **Course**: [Git & GitHub Bootcamps (Udemy)](https://www.udemy.com/course/git-and-github-bootcamp/)\n"
            "• **Free**: [Pro Git Book](https://git-scm.com/book/en/v2)\n"
            "• **Cheatsheet**: [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)"
        )

    elif "typescript" in msg or "ts" in msg:
        response = (
            "📘 **TypeScript Resources**\n"
            "• **Course**: [Understanding TypeScript (Udemy)](https://www.udemy.com/course/understanding-typescript/)\n"
            "• **Free**: [TypeScript Handbook](https://www.typescriptlang.org/docs/)\n"
            "• **Practice**: [Total TypeScript](https://www.totaltypescript.com/tutorials)"
        )

    elif "flutter" in msg or "android" in msg or "ios" in msg or "mobile" in msg:
        response = (
            "📱 **Mobile Development**\n"
            "• **Course**: [Flutter & Dart - The Complete Guide (Udemy)](https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/)\n"
            "• **Free**: [Flutter Docs](https://docs.flutter.dev/)\n"
            "• **Android**: [Android Developers](https://developer.android.com/)"
        )

    elif "angular" in msg or "vue" in msg:
        response = (
            "🅰️ **Angular & Vue Resources**\n"
            "• **Angular**: [Angular Docs](https://angular.io/docs)\n"
            "• **Vue**: [Vue.js Docs](https://vuejs.org/guide/introduction.html)\n"
            "• **Course**: Check Udemy for 'Angular - The Complete Guide' (Max S.)"
        )
    
    # --- 2. Fallback to Gemini AI ---
    
    if response:
        # We found a hardcoded response, send it.
        await context.bot.send_message(chat_id=chat_id, text=response, parse_mode='Markdown', disable_web_page_preview=True)
    elif model:
        # Use Gemini
        try:
            chat_response = model.generate_content(msg)
            safe_response = chat_response.text 
            # Check length to avoid telegram limits (4096 chars)
            if len(safe_response) > 4000:
                 safe_response = safe_response[:3900] + "...(truncated)"
            
            # Add a small signature
            safe_response += "\n\n✨ *Generated by AI*"
            
            await context.bot.send_message(chat_id=chat_id, text=safe_response, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Gemini Error: {e}")
            await context.bot.send_message(chat_id=chat_id, text="⚠ I'm having trouble thinking right now. Try again later!", parse_mode='Markdown')
            
    else:
        # No keyword match AND no API key found
        fallback_response = (
            "That's interesting! 🤔\n"
            "I noticed you said something about '{}'.\n"
            "I'm not fully sure, but try typing language names like **Python**, **Java**, or **React** to get specific links!".format(msg[:20])
         )
        await context.bot.send_message(chat_id=chat_id, text=fallback_response, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == '__main__':
    # Fix for Windows loop policy
    import asyncio
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        exit(1)

    import pytz
    from telegram.ext import Defaults
    
    defaults = Defaults(tzinfo=pytz.UTC)
    application = ApplicationBuilder().token(TOKEN).defaults(defaults).job_queue(None).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('contact', contact_info))
    
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    keep_alive()  # Start the web server
    application.run_polling()
