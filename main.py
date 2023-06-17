import tkinter
from tkinter import messagebox
import requests
import random

current_key=0
mode=0

url = "API_url"

headers = {
	"X-RapidAPI-Key": "API_key",
	"X-RapidAPI-Host": "API_host"
    }
response = requests.get(url, headers=headers)
text=response.json()

value_of_N_response=requests.get("API_url",headers=headers)
N_text=value_of_N_response.json()
for i in range(len(N_text)):
    # print(quesN[i])
    if N_text[i]["Name"]=="chinglemba":
        ques_key=i
N=N_text[ques_key]["No_of_questions"]

mode=0
q = []
questions = []
count = 0
while count <= N:
    for i in range(N):
        j = random.randint(0, len(text) - 1)
        if j in q:
            continue
        else:
            q.append(j)
    count = count + 1

current_question = 0
score = 0

def set_compete_mode(current_window=None):
    global mode
    mode=1
    if current_window:
        current_window.destroy()
    # print(mode)
    
    start_quiz()

def start_quiz(current_window=None):
    global mode
    # print(mode)
    # destroying if current_window is active
    # print(compete_mode)
    if current_window:
        current_window.destroy()
    for j in range(N):
        i = q[j]
        question_data = {
            "Question": text[i]["Question"],
            "Options": [],
            "Answer": text[i]["Answer"]
            }
        for option_key in ["OptA", "OptB", "OptC", "OptD"]:
            if option_key in text[i]:
                question_data["Options"].append(text[i][option_key])
                # print(text[i][option_key])
        questions.append(question_data)
        # print(questions)
        # print(question_data)
     
    def check_answer(selected_option):
        global current_question, score
        # print(questions[current_question]["Ans"])
        if selected_option == questions[current_question]["Answer"]:
            score += 1
        current_question += 1
        if current_question < len(questions):
            question_label.config(text=questions[current_question]["Question"])
            update_option_buttons()
        else:
            show_final_score()

    def show_final_score():
        messagebox.showinfo("Quiz completed", f"Quiz completed!\nYour final score is: {score}/{len(questions)}")
        # print("mode=",mode)
        # print("final score_current_key=",current_key)
        # print("score=",score)

        if mode==1:
            payload = {
    	        "Score": score,
	            "c_quiz_users_id": current_key
            }
            headers = {
                "content-type": "application/x-www-form-urlencoded",
        	    # "content-type": "application/json",
    	        "X-RapidAPI-Key": "API_key",
    	        "X-RapidAPI-Host": "API_host"
            }
            response = requests.post("https://API_host/add_C_Score", data=payload, headers=headers)
        quiz_window.destroy()

    def update_option_buttons():
        options = questions[current_question]["Options"]
        num_options = len(options)
        for i in range(num_options):
            if i >= len(option_buttons):
                # print(options[i])
                button = tkinter.Button(quiz_window, text=options[i], font=("Arial", 14),width=50,command=lambda i=i: check_answer(option_letters[i]))
                button.pack(pady=10)
                option_buttons.append(button)
            else:
                option_buttons[i].config(text=options[i])

    # creating the window
    quiz_window = tkinter.Tk()
    quiz_window.title("Quiz")
    # quiz_window.geometry("800x400")
    quiz_window.configure(bg='#333333')
    quiz_window.resizable(False, False)
    screen_width = quiz_window.winfo_screenwidth()
    screen_height = quiz_window.winfo_screenheight()
    # Calculate the window width and height
    window_width = 800
    window_height = 400

    # Calculate the x and y coordinates for centering the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    quiz_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # creating question label
    question_label = tkinter.Label(quiz_window, text=questions[current_question]["Question"],font=("Arial", 17),bg='#87CEEB', fg='black',pady=20, wraplength=570,borderwidth=5)
    question_label.pack(pady=15)

    # creating the option buttons
    option_buttons = []
    option_letters=["A","B","C","D"]
    update_option_buttons()

    # start the tkinter event loop
    quiz_window.mainloop()

def leaderboard(main_window):
    main_window.destroy()
    leaderboard_window=tkinter.Tk()
    leaderboard_window.title("C Programming Leaderboard")
    leaderboard_window.configure(bg='#333333')
    leaderboard_window.resizable(False, False)
    screen_width = leaderboard_window.winfo_screenwidth()
    screen_height = leaderboard_window.winfo_screenheight()
    # Calculate the window width and height
    window_width = 500
    window_height = 320

    # Calculate the x and y coordinates for centering the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    leaderboard_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
    leader_frame=tkinter.Frame()
    leader_frame.configure(bg='#333333',pady=20)

    headers = {
            "X-RapidAPI-Key": "API_key",
            "X-RapidAPI-Host": "API_host"
        }
    response = requests.get("API_url", headers=headers)
    data = response.json()
    leader_board = sorted(data, key=lambda x: x["Score"], reverse=True)
    name=[]
    score=[]
    # print(leader_board)
    for i in range(3):
        name.append(leader_board[i]["Name"])
        score.append(leader_board[i]["Score"])
        # print(name[i],score[i])

    #creating the widgets
    leader_label=tkinter.Label(leader_frame,text='TOP THREE SCORERS',width=40,font=("Arial", 15),bg='#533357', fg='yellow',pady=10)
    first_name=tkinter.Label(leader_frame,text=f'1st: {name[0]} with {score[0]} scores',font=("Arial", 15),bg='#333333', fg='white',pady=5)
    second_name=tkinter.Label(leader_frame,text=f'2nd: {name[1]} with {score[1]} scores',font=("Arial", 15),bg='#333333', fg='white',pady=5)
    third_name=tkinter.Label(leader_frame,text=f'3rd: {name[2]} with {score[2]} scores',font=("Arial", 15),bg='#333333', fg='white',pady=5)
    back_menu_button=tkinter.Button(leader_frame,width=30,text="Back to main menu",pady=5,font=("Arial", 15), command=lambda:main_menu(leaderboard_window))

    #placing the widgets
    leader_label.grid(row=0,column=0,columnspan=2,pady=10)
    first_name.grid(row=1,column=0,columnspan=2,pady=5)
    second_name.grid(row=2,column=0,columnspan=2,pady=5)
    third_name.grid(row=3,column=0,columnspan=2,pady=5)
    back_menu_button.grid(row=4,column=0,columnspan=2,pady=5)

    # menu_label.pack()
    leader_frame.pack()

def main_menu(current_window=None):
    if current_window:
        current_window.destroy()
    # print("Main menu_current key=",current_key)
    main_window=tkinter.Tk()
    main_window.title("C Programming Quiz")
    main_window.configure(bg='#333333')
    main_window.resizable(False, False)
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    # Calculate the window width and height
    window_width = 500
    window_height = 280

    # Calculate the x and y coordinates for centering the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    main_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    menu_frame=tkinter.Frame()
    menu_frame.configure(bg='#333333',pady=20)

    #creating the widgets
    menu_label=tkinter.Label(menu_frame,text='Main menu',font=("Arial", 15),bg='#333333', fg='red',pady=10)
    practice_button=tkinter.Button(menu_frame,width=30,text="Practice Session",font=("Arial", 15),command=lambda:start_quiz(main_window))
    compete_button=tkinter.Button(menu_frame,width=30,text="Competition mode",font=("Arial", 15),command=lambda:set_compete_mode(main_window))
    leaderboard_button=tkinter.Button(menu_frame,width=30,text="Leaderboard",font=("Arial", 15), command=lambda:leaderboard(main_window))
    
    #placing the widgets
    menu_label.grid(row=0,column=0,columnspan=2,pady=10)
    practice_button.grid(row=1,column=0,pady=5)
    compete_button.grid(row=2,column=0,pady=5)
    leaderboard_button.grid(row=3,column=0,pady=5)

    # menu_label.pack()
    menu_frame.pack()

    main_window.mainloop()

def login():
    global current_key
    url="API_url"
    headers = {
	    "X-RapidAPI-Key": "API_key",
	    "X-RapidAPI-Host": "API_host"
        }
    user_response=requests.get("API_url", headers=headers)
    user_response_text=user_response.json()
    userN=len(user_response_text)
    current_user=username_entry.get()
    current_password=password_entry.get()
    flag=0
    for i in range(userN):
        ref_user=user_response_text[i]["Name"]
        ref_pwd=user_response_text[i]["Auth"]
        if current_user==ref_user and current_password==ref_pwd:
            # messagebox.showinfo(title="Login Success",message="You have logged in successfully")
            current_key=user_response_text[i]["id"]
            # print("current key : ",current_key)

            flag=flag+1
            window.destroy()
            main_menu()

    if flag==0:
        messagebox.showinfo(title="Login failed",message="Invalid Login")
    

window = tkinter.Tk()
window.title("C Programming Quiz")
window.configure(bg='#333333')
window.resizable(False, False)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the window width and height
window_width = 500
window_height = 255
# Calculate the x and y coordinates for centering the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f'{window_width}x{window_height}+{x}+{y}')
label = tkinter.Label(window, text="Login")
#label.pack()
frame=tkinter.Frame()
frame.configure(bg='#333333',pady=20)

#creating the widgets
login_label=tkinter.Label(frame,text='Enter your credentials:',font=("Arial", 15),bg='#333333', fg='red',pady=10)
username_label=tkinter.Label(frame,text='User name',bg='#333333', font=("Arial", 15),fg='white')
username_entry=tkinter.Entry(frame,font=("Arial", 15))
password_entry=tkinter.Entry(frame,show="*",font=("Arial", 15))
password_label=tkinter.Label(frame,text='Password',bg='#333333',font=("Arial", 15),fg='white')
login_button=tkinter.Button(frame,text="Login",font=("Arial", 15), command=login)

#placing the widgets
login_label.grid(row=0,column=0,columnspan=2,pady=10)
username_label.grid(row=1,column=0,pady=5)
username_entry.grid(row=1,column=1)
password_label.grid(row=2,column=0,pady=5)
password_entry.grid(row=2,column=1)
login_button.grid(row=4,column=0,columnspan=2,pady=10)

frame.pack()

window.mainloop()
