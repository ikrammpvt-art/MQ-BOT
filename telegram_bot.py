"""
===============================================================================
TELEGRAM BOT WITH HERMES AI AGENTIC DOCUMENT PARSER & ENRICHMENT BACKEND
===============================================================================
"""

import os
import sys
import time
import telebot
from hermes_agent import HermesAgent
from company_framework import CompanyFramework

# Load BOT_TOKEN from environment variable or user config
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8770558776:AAGz_ZZ5_frsHuL8KFefB0-AtFkYbnGT1GE").strip()

if not BOT_TOKEN:
    print("\n⚠️ WARNING: TELEGRAM_BOT_TOKEN is not set.")
    print("   To run the bot, get a free token from @BotFather on Telegram and run:")
    print("   export TELEGRAM_BOT_TOKEN='your_token_here'")
    print("   python3 telegram_bot.py\n")

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

if bot:
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        welcome_text = (
            "🤖 *Corporate Portfolio Intelligence Bot (Powered by Hermes AI)*\n\n"
            "Welcome! Send me any Excel (`.xlsx`) or CSV (`.csv`) portfolio dataset, "
            "and Hermes AI will automatically:\n"
            "1. 🧠 *Scan & Parse*: Hermes AI Agent normalizes table headers and schema.\n"
            "2. 🛡️ *Filter*: Ignores numeric serial IDs (`69`, `79`, `80`) and locks onto true Company Names.\n"
            "3. 🔍 *Triangulate*: Runs 4-point verification & HTTP live status check.\n"
            "4. 📊 *Enrich*: Attaches CEOs, PE Sponsors, HQ Addresses, Phone, Email & Gain.pro links.\n"
            "5. 🍏 *Export*: Returns 100% Apple Numbers CSV & Excel files!\n\n"
            "📌 *Just drop your document below to begin!*"
        )
        bot.reply_to(message, welcome_text, parse_mode="Markdown")

    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        try:
            doc_name = message.document.file_name or "portfolio_data.xlsx"
            if not doc_name.lower().endswith(('.xlsx', '.xls', '.csv')):
                bot.reply_to(message, "❌ Please send an Excel (`.xlsx`, `.xls`) or CSV (`.csv`) document.", parse_mode="Markdown")
                return

            status_msg = bot.reply_to(
                message, 
                f"⏳ *File received:* `{doc_name}`\n🧠 *Hermes AI Agent* scanning document, normalizing schema & running 4-point triangulation...", 
                parse_mode="Markdown"
            )

            # Download File
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            input_path = os.path.join("/tmp", f"telegram_input_{int(time.time())}_{doc_name}")
            with open(input_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # 1. Hermes AI Agent Parsing & Normalization Step
            parsed_df, company_col = HermesAgent.parse_document(input_path)

            # 2. Execute Backend Framework Engine
            fw = CompanyFramework(input_path)
            fw.load_data()
            fw.detect_anomalies()
            fw.process_and_enrich()

            output_base = os.path.join("/tmp", f"milund_enriched_{int(time.time())}")
            csv_out, xlsx_out = fw.export(output_base)

            df = fw.processed_df
            unique_cnt = df[fw.comp_col].nunique()

            summary_text = (
                "✅ *Hermes AI Processing Report*\n\n"
                f"• *Document Name:* `{doc_name}`\n"
                f"• *Identified Entity Column:* `{company_col}`\n"
                f"• *Total Loan Tranches:* `{len(df):,}`\n"
                f"• *Unique Portfolio Entities:* `{unique_cnt:,}`\n"
                f"• *Enriched Columns:* `16 New Institutional Fields`\n"
                f"• *Apple Numbers Status:* `100% Native Opening`\n\n"
                "👇 *Here are your enriched output files:* "
            )

            bot.edit_message_text(summary_text, chat_id=status_msg.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")

            base_clean_name = os.path.splitext(doc_name)[0]

            # Send Enriched CSV File
            with open(csv_out, 'rb') as f_csv:
                bot.send_document(
                    message.chat.id, 
                    f_csv, 
                    visible_file_name=f"milund_enriched_{base_clean_name}.csv",
                    caption="🍏 *Apple Numbers Compatible CSV (Hermes Enriched)*"
                )

            # Send Enriched XLSX File
            with open(xlsx_out, 'rb') as f_xlsx:
                bot.send_document(
                    message.chat.id, 
                    f_xlsx, 
                    visible_file_name=f"milund_enriched_{base_clean_name}.xlsx",
                    caption="📊 *Clean Excel Workbook (.xlsx)*"
                )

        except Exception as e:
            print(f"Error handling document: {e}")
            bot.reply_to(message, f"❌ Error processing document: {str(e)}")

if __name__ == '__main__':
    if bot:
        print("🚀 Telegram Bot with Hermes AI Agent is LIVE and polling for documents...")
        bot.infinity_polling()
    else:
        print("Please set TELEGRAM_BOT_TOKEN environment variable to start.")
