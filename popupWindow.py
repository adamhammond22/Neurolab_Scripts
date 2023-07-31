from tkinter import *

# define the global restartProgram variable. This is used by excelFormat.py to understand whether
# it should terminate or not.
global restartProgram


# this function is executed by our popup bottons, taking a string option input, and the root input
# it will destroy the root when completed, ending the mainloop it's attached to
def choice(option: str, ourRoot):
	if option == "yes":
		global restartProgram
		restartProgram = True
		print("\nProgram Continuing")
  
	else:
		print("\nTerminating")


	# destroy our root reference to break the main loop, and continue or terminate
	ourRoot.destroy()

# this function creates a popup window, asking if the program should continue
def initiatePopup(ourRoot):

	def onClose():
		print("\nTerminating")
		ourRoot.destroy()


	# global popupWindow

	# style our window, and bring it to the front
	popupWindow = Toplevel(ourRoot)
	popupWindow.title("Program Finished")
	popupWindow.geometry("300x150")
	popupWindow.config(bg="white")
	popupWindow.protocol("WM_DELETE_WINDOW", onClose)

	popupWindow_label = Label(popupWindow, text="Would You Like To Continue?", bg="white", fg="black", font=("helvetica", 14))
	popupWindow_label.pack(pady=10)
	 
	# make a frame to pack our buttons into
	my_frame = Frame(popupWindow, bg="white")
	my_frame.pack(pady=5)

	# create the buttons
	yes = Button(my_frame, text="YES", command=lambda: choice("yes", ourRoot), bg="green", font=("helvetica", 14))
	yes.grid(row=0, column=1, padx=30)

	no = Button(my_frame, text="NO", command=lambda: choice("no", ourRoot), bg="orange", font=("helvetica", 14))
	no.grid(row=0, column=2, padx=30)

