#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tempfile
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import random
import matplotlib.pyplot as plt

# تهيئة التعرف على الصوت
recognizer = sr.Recognizer()

def get_audio():
    with sr.Microphone() as source:
        print("تحدث الآن...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ar-SA")
            print("لقد قلت: " + text)
            return text
        except sr.UnknownValueError:
            print("لم يتم التعرف على الصوت")
            return None
        except sr.RequestError:
            print("خطأ في الخدمة")
            return None

def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        print(f"خطأ في الحساب: {e}")
        return None

def generate_similar_equations(expression, num=3):
    # Split the expression into components
    tokens = expression.split()
    similar_equations = []
    for _ in range(num):
        new_expr = ""
        for token in tokens:
            if token.isdigit():
                # Slightly alter the number
                new_num = int(token) + random.choice([-1, 1, 2, -2])
                new_expr += str(new_num) + " "
            elif token in ['+', '-', '*', '/']:
                # Randomly choose an operator
                new_operator = random.choice(['+', '-', '*', '/'])
                new_expr += new_operator + " "
            else:
                new_expr += token + " "
        similar_equations.append(new_expr.strip())
    return similar_equations

def text_to_speech(text):
    tts = gTTS(text=text, lang='ar')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        temp_filename = fp.name
        tts.save(temp_filename)
    
    pygame.mixer.init()
    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Add a small delay to avoid high CPU usage
    
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    os.remove(temp_filename)

if name == "main":
    exit_keyword = "انتهيت"
    train_keyword = "تدريب"
    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        attempts += 1

        # الحصول على المدخلات الصوتية
        expression = get_audio()
        if expression:
            # Check for exit keyword
            if exit_keyword in expression:
                print("تم إنهاء البرنامج.")
                text_to_speech("تم إنهاء البرنامج.")
                break

            # Check for training keyword
            if train_keyword in expression:
                print("بدء التدريب على المعادلات المشابهة.")
                text_to_speech("بدء التدريب على المعادلات المشابهة.")
                
                while True:
                    # الحصول على المدخلات الصوتية للتدريب
                    train_expression = get_audio()
                    if train_expression:
                        # Check for exit keyword
                        if exit_keyword in train_expression:
                            print("تم إنهاء التدريب.")
                            text_to_speech("تم إنهاء التدريب.")
                            break
                        
                        # حساب الناتج
                        train_result = calculate(train_expression)
                        if train_result is not None:
                            print(f"الناتج هو: {train_result}")
                            # تحويل الناتج إلى صوت
                            text_to_speech(f"الناتج هو: {train_result}")
# إنشاء وعرض المعادلات المشابهة
                            similar_equations = generate_similar_equations(train_expression)
                            for eq in similar_equations:
                                print(f"معادلة مشابهة: {eq}")
                                text_to_speech(f"معادلة مشابهة: {eq}")
                                
                                # الحصول على إجابة المستخدم
                                user_answer = get_audio()
                                if user_answer:
                                    try:
                                        user_result = float(user_answer)
                                        correct_result = calculate(eq)
                                        if user_result == correct_result:
                                            feedback = "أحسنت الإجابة صحيحة"
                                            print(feedback)
                                            text_to_speech(feedback)
                                        else:
                                            feedback = f"الإجابة خطأ والناتج الصحيح هو {correct_result}"
                                            print(feedback)
                                            text_to_speech(feedback)
                                    except ValueError:
                                        feedback = "لم يتم التعرف على الإجابة"
                                        print(feedback)
                                        text_to_speech(feedback)

                continue  # Restart the main loop after training

            # حساب الناتج للمعادلة الرئيسية
            result = calculate(expression)
            if result is not None:
                print(f"الناتج هو: {result}")
                # تحويل الناتج إلى صوت
                text_to_speech(f"الناتج هو: {result}")


# In[ ]:




