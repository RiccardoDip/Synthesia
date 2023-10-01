import customtkinter
import tkinter as tk
from tkinter import *
import tkinterdnd2 as tkdnd
from PIL import Image
from tkinter import filedialog

import subprocess
import sys
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # disable GPU for gansynth
# this is necessary due to problems combining tf compat v1 and v2

basic_arg = sys.argv[0]
sys.path.append("magenta")
sys.path.append("Music-Visualizer")
# import gansynth
# import visualizer

midway_output_dir = "midway"

model_gansynth = gansynth.setup()

input("Press Enter to continue...")

gansynth.set_output_dir(midway_output_dir)
audio_note_list = None
z_preview = None
notes = None


def select_midi_seq():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path.endswith(".mid"):
        midi_path.configure(text=file_path)
        print(midi_path._text)
        alertWF.configure(
            app, text="MIDI file loaded correctly", text_color="lightgreen"
        )
        alertWF.place(relx=0.5, rely=0.15, anchor=CENTER)
        instButton.configure(state="normal")

    else:
        alertWF.configure(app, text="Please choose a MIDI FIle", text_color="red")
        alertWF.place(relx=0.5, rely=0.15, anchor=CENTER)
        instButton.configure(state=DISABLED)
    root.destroy()


def DisplayMidiFile(event):
    file_path = event.data
    if file_path[0] == "{" and file_path[len(file_path) - 1] == "}":
        file_path = file_path[1 : len(file_path) - 1]

    if file_path.endswith(".mid"):
        midi_path.configure(text=file_path)
        print(midi_path._text)
        alertWF.configure(
            app, text="MIDI file loaded correctly", text_color="lightgreen"
        )
        alertWF.place(relx=0.5, rely=0.15, anchor=CENTER)
        instButton.configure(state="normal")

    else:
        alertWF.configure(app, text="Please choose a MIDI FIle", text_color="red")
        alertWF.place(relx=0.5, rely=0.15, anchor=CENTER)
        instButton.configure(state=DISABLED)
    print(file_path)


def DisplayImage1(event):
    print("entrato")
    if event.data[0] == "{" and event.data[len(event.data) - 1] == "}":
        event.data = event.data[1 : len(event.data) - 1]
    print(event.data)
    # check the file holds txt extension
    if (
        event.data.endswith(".png")
        or event.data.endswith(".jpg")
        or event.data.endswith(".jpeg")
    ):
        print("entrato2")
        im1 = Image.open(event.data)
        image1 = customtkinter.CTkImage(im1, size=(100, 100))
        image_display1.configure(
            app, image=image1, text=None, width=100, height=100, state=DISABLED
        )
        image_display1.place(relx=0.2, rely=0.57, anchor=CENTER)
        im1.save("style_ref/00.png")
        textbox1.place_forget()


def DisplayImage2(event):
    print("entrato")
    if event.data[0] == "{" and event.data[len(event.data) - 1] == "}":
        event.data = event.data[1 : len(event.data) - 1]
    print(event.data)
    # check the file holds txt extension
    if (
        event.data.endswith(".png")
        or event.data.endswith(".jpg")
        or event.data.endswith(".jpeg")
    ):
        print("entrato2")
        im2 = Image.open(event.data)
        image2 = customtkinter.CTkImage(im2, size=(100, 100))
        image_display2.configure(
            app, image=image2, text=None, width=100, height=100, state=DISABLED
        )
        image_display2.place(relx=0.4, rely=0.57, anchor=CENTER)
        im2.save("style_ref/01.png")
        textbox2.place_forget()


def DisplayImage3(event):
    print("entrato")
    if event.data[0] == "{" and event.data[len(event.data) - 1] == "}":
        event.data = event.data[1 : len(event.data) - 1]
    print(event.data)
    # check the file holds txt extension
    if (
        event.data.endswith(".png")
        or event.data.endswith(".jpg")
        or event.data.endswith(".jpeg")
    ):
        print("entrato2")
        im3 = Image.open(event.data)
        image3 = customtkinter.CTkImage(im3, size=(100, 100))
        image_display3.configure(
            app, image=image3, text=None, width=100, height=100, state=DISABLED
        )
        image_display3.place(relx=0.6, rely=0.57, anchor=CENTER)
        im3.save("style_ref/02.png")
        textbox3.place_forget()


def DisplayImage4(event):
    print("entrato")
    if event.data[0] == "{" and event.data[len(event.data) - 1] == "}":
        event.data = event.data[1 : len(event.data) - 1]
    print(event.data)
    # check the file holds txt extension
    if (
        event.data.endswith(".png")
        or event.data.endswith(".jpg")
        or event.data.endswith(".jpeg")
    ):
        print("entrato2")
        im4 = Image.open(event.data)
        image4 = customtkinter.CTkImage(im4, size=(100, 100))
        image_display4.configure(
            app, image=image4, text=None, width=100, height=100, state=DISABLED
        )
        image_display4.place(relx=0.8, rely=0.57, anchor=CENTER)
        im4.save("style_ref/03.png")
        textbox4.place_forget()

# def append_list(arg, list):
#     sys.argv.append(arg)
#     for num in list:
#         sys.argv.append(str(num))
def append_list(arg, list):
    to_append = arg
    for num in list:
        to_append += f" {num}"
    return to_append


def generation_process():
    global audio_note_list, z_preview, notes

    fname = "synthesia"
    if inst_label._text == 4:
        if transition1_value._text == transition2_value._text:
            textboxInfo.configure(
                app, text="Transition values must be different!", text_color="red"
            )
            app.update_idletasks()
            print("Values must be different!")
            return
    textboxInfo.configure(app,text="Creating Audio", text_color="white")
    app.update_idletasks()
    instr_list, time_list = create_sequences()

    # gansynth.generate_audio(
    #     model_gansynth, z_preview, notes, instr_list, time_list, f'{fname}_gansynth'
    # )

    # os.system('__main__.py -i gansynth/samples/generated_clip_1.mp3 -ff /usr/lib/ffmpeg')
    textboxInfo.configure(app,text="Creating Video Spectrogram", text_color="white")
    app.update_idletasks()

    sys.argv = [basic_arg]
    sys.argv += [
        "-i",
        f"{midway_output_dir}/{fname}_gansynth.mp3",
        "-o",
        f"{midway_output_dir}",
    ]
    if sys.platform == "linux" or sys.platform == "linux2":
        sys.argv += ["-ff", "/usr/bin/ffmpeg"]
    elif sys.platform == "darwin":
        sys.argv += ["-ff", "/usr/local/Cellar/ffmpeg/6.0/bin/ffmpeg"]
    #visualizer.main()

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    textboxInfo.configure(app,text="Applying style transfer", text_color="white")
    app.update_idletasks()


    # import style_frames
    # sys.argv = [basic_arg]
    # sys.argv += ['-i', f'../Music-Visualizer/output/{fname}.mp4']
    # append_list('-ss', instr_list)
    # append_list('-ts', time_list)
    # style_frames.module_run()
    # this unfortunately does not work because of the previews use of
    # tf.compat.v1 for gansynth, using a different process instead
    arguments = (
        f"-i {midway_output_dir}/{fname}_gansynth_spectr.mp4 -d output -o synthesia_art"
        # f"-i /Users/macdonald/Desktop/CPAC/real-time-style-transfer/scope_intero.mp4 -d {cwd}/output -o synthesia_art"
    )
    arguments += append_list(" -ss", instr_list)
    arguments += append_list(" -ts", time_list)
    arguments += f" -mf {midway_output_dir} -sf style_ref"
    arguments += " --fps 10"
    #arguments += f" -a {midway_output_dir}/{fname}_gansynth.mp3 --no_audio"
    # os.system(f"python style-transfer-video-processor/style_frames.py {arguments}")
    command = ["python", "style-transfer-video-processor/style_frames.py"]
    command += arguments.split(" ")
    # os.system(f"python style-transfer-video-processor/style_frames.py {arguments}")
    subprocess.call(command)
    textboxInfo.configure(app,text="Video saved in the ouput folder", text_color="white")
    app.update_idletasks()


def generate():
    global audio_note_list, z_preview, notes
    try:
        textboxInfo.configure(app,text="Generating instruments", text_color="white")
        app.update_idletasks()
        print("clicked")

        num_instr = inst_label._text
        midi_path_str = midi_path._text
        print(f"num: {num_instr}")
        print(f"midi path: {midi_path_str}")

        # audio_note_list, z_preview, notes = gansynth.generate_instruments(
        #     model_gansynth, midi_path_str, num_instr
        # )

        if display_inst.get() == False:
            # trans_label.pack()

            if inst_label._text == 2:
                Inst2Btn.place(relx=0.4, rely=0.40, anchor=CENTER)
                Inst1Btn.place(relx=0.2, rely=0.40, anchor=CENTER)
                gsButton.place(relx=0.5, rely=0.75, anchor=CENTER)
                textbox1.place(relx=0.2, rely=0.55, anchor=CENTER)
                textbox2.place(relx=0.4, rely=0.55, anchor=CENTER)
                textboxInfo.configure(app,text="Instruments Generated! Drop style images, otherwise the default ones will be used", text_color="white")
                app.update_idletasks()

                if Inst3Btn.winfo_viewable() == 1:
                    Inst3Btn.place_forget()
                    transition2.place_forget()
                    textbox3.place_forget()
                    image_display3.place_forget()

                if Inst4Btn.winfo_viewable() == 1:
                    Inst4Btn.place_forget()
                    transition3.place_forget()
                    textbox4.place_forget()
                    image_display4.place_forget()

                if image_display1.winfo_viewable() == 1:
                    textbox1.place_forget()
                if image_display2.winfo_viewable() == 1:
                    textbox2.place_forget()
                if transition1.winfo_viewable() == 1:
                    transition1.place_forget()

            if inst_label._text == 3:
                gsButton.place_forget()
                Inst1Btn.place(relx=0.2, rely=0.40, anchor=CENTER)
                transition1.place(relx=0.4, rely=0.45, anchor=CENTER)
                Inst2Btn.place(relx=0.4, rely=0.40, anchor=CENTER)
                Inst3Btn.place(relx=0.6, rely=0.40, anchor=CENTER)
                gsButton.place(relx=0.5, rely=0.75, anchor=CENTER)
                textbox1.place(relx=0.2, rely=0.55, anchor=CENTER)
                textbox2.place(relx=0.4, rely=0.55, anchor=CENTER)
                textbox3.place(relx=0.6, rely=0.55, anchor=CENTER)

                if Inst4Btn.winfo_viewable() == 1:
                    Inst4Btn.place_forget()
                    transition3.place_forget()
                    textbox4.place_forget()
                    image_display4.place_forget()

                if image_display1.winfo_viewable() == 1:
                    textbox1.place_forget()
                if image_display2.winfo_viewable() == 1:
                    textbox2.place_forget()
                if image_display3.winfo_viewable() == 1:
                    textbox3.place_forget()
                if transition2.winfo_viewable() == 1:
                    transition2.place_forget()
                textboxInfo.configure(app,text="Instruments Generated! Select transition time and drop style images, otherwise the default ones will be used", text_color="white")
                app.update_idletasks()

            if inst_label._text == 4:
                gsButton.place_forget()
                Inst1Btn.place(relx=0.2, rely=0.40, anchor=CENTER)
                transition1.place(relx=0.4, rely=0.45, anchor=CENTER)
                Inst2Btn.place(relx=0.4, rely=0.40, anchor=CENTER)
                # trans_label.pack()
                transition2.place(relx=0.6, rely=0.45, anchor=CENTER)
                Inst3Btn.place(relx=0.6, rely=0.40, anchor=CENTER)
                # transition3.place(relx=0.8,rely=0.55,anchor=CENTER)
                Inst4Btn.place(relx=0.8, rely=0.40, anchor=CENTER)
                textbox1.place(relx=0.2, rely=0.55, anchor=CENTER)
                textbox2.place(relx=0.4, rely=0.55, anchor=CENTER)
                textbox3.place(relx=0.6, rely=0.55, anchor=CENTER)
                textbox4.place(relx=0.8, rely=0.55, anchor=CENTER)
                gsButton.place(relx=0.5, rely=0.75, anchor=CENTER)
                textboxInfo.configure(app,text="Instruments Generated! Select transition time and drop style images, otherwise the default ones will be used", text_color="white")
                app.update_idletasks()
            display_inst.set(True)

            if image_display1.winfo_viewable() == 1:
                textbox1.place_forget()
            if image_display2.winfo_viewable() == 1:
                textbox2.place_forget()
            if image_display3.winfo_viewable() == 1:
                textbox3.place_forget()
            if image_display4.winfo_viewable() == 1:
                textbox4.place_forget()
    except:
        print("error")


def updatelabel(label):
    try:
        inst_label.configure(text=int(label))
        display_inst.set(False)
    except:
        inst_label.configure(text="2")


def updateTransition1(choice):
    try:
        transition1_value.configure(text=float(choice))
        print(transition1_value._text)
    except:
        transition1_value.configure(text="error")


def updateTransition2(choice):
    try:
        transition2_value.configure(text=float(choice))
        print(transition2_value._text)
    except:
        transition2_value.configure(text="error")


def updateTransition3(choice):
    try:
        transition3_value.configure(text=float(choice))
        print(transition3_value._text)
    except:
        transition3_value.configure(text="error")


def create_sequences():
    try:
        time_list = [0]
        instr_list = [0]
        if inst_label._text == 2:
            time_list.append(1)
            instr_list.append(1)

        if inst_label._text == 3:
            time_list.append(transition1_value._text)
            time_list.append(1)
            instr_list += [1, 2]

        if inst_label._text == 4:
            time_list.append(transition1_value._text)
            time_list.append(transition2_value._text)
            time_list.append(1)

            time_list.sort()
            if transition1_value._text == time_list[1]:
                instr_list += [1, 2]
            else:
                instr_list += [2, 1]
            instr_list.append(3)

        print(time_list)
        print(instr_list)
    except:
        print("error")

    return instr_list, time_list


app = tkdnd.Tk()
app.geometry("780x680")
app.resizable(0, 0)
app.title("Synthesia")
app.config(bg="#39393F")


image_display1 = customtkinter.CTkButton(
    app, text=None, width=100, height=100, state=DISABLED
)
image_display2 = customtkinter.CTkButton(
    app, text=None, width=100, height=100, state=DISABLED
)
image_display3 = customtkinter.CTkButton(
    app, text=None, width=100, height=100, state=DISABLED
)
image_display4 = customtkinter.CTkButton(
    app, text=None, width=100, height=100, state=DISABLED
)

display_inst = customtkinter.BooleanVar(app, False)
title = customtkinter.CTkLabel(app, text="SYNTHESIA",text_color="white")
title.place(relx=0.5, rely=0.03, anchor=CENTER)

frame = Frame(app, background="#39393F")
frame.place(relx=0.5, rely=0.10, anchor=CENTER)

textboxMidi = customtkinter.CTkLabel(
    frame,
    width=350,
    height=40,
    text="Drop MIDI File Here",
    text_color="white",
    bg_color="grey",
)
textboxMidi.pack(side=LEFT)
textboxMidi.drop_target_register(tkdnd.DND_FILES)
textboxMidi.dnd_bind("<<Drop>>", DisplayMidiFile)

alert = customtkinter.CTkLabel(app, text="")
alertWF = customtkinter.CTkLabel(app, text="")
midi_path = customtkinter.CTkLabel(app, text="")


path_var = customtkinter.StringVar()

inst_label = customtkinter.CTkLabel(
    app, text="Select number of random instruments", text_color="white"
)
inst_label.place(relx=0.5, rely=0.19, anchor=CENTER)


inst_label = customtkinter.CTkLabel(app, text=2, text_color="white")
inst_label.place(relx=0.5, rely=0.22, anchor=CENTER)

inst_slider = customtkinter.CTkSlider(
    app, from_=2, to=4, number_of_steps=2, command=updatelabel, width=400
)
inst_slider.set(0)
inst_slider.place(relx=0.5, rely=0.25, anchor=CENTER)


instButton = customtkinter.CTkButton(
    app, text="Generate Instruments", command=generate, state=DISABLED
)
instButton.place(relx=0.5, rely=0.30, anchor=CENTER)

Inst1Btn = customtkinter.CTkButton(
    app, text="Inst.1", command=lambda: gansynth.play_audio_array(audio_note_list[0])
)
Inst2Btn = customtkinter.CTkButton(
    app, text="Inst.2", command=lambda: gansynth.play_audio_array(audio_note_list[1])
)
Inst3Btn = customtkinter.CTkButton(
    app, text="Inst.3",  command=lambda: gansynth.play_audio_array(audio_note_list[2])
)
Inst4Btn = customtkinter.CTkButton(
    app, text="Inst.4", command=lambda: gansynth.play_audio_array(audio_note_list[3])
)

generating = customtkinter.BooleanVar(app, False)
generated = customtkinter.BooleanVar(app, False)

trans_label = customtkinter.CTkLabel(app, text="Select the transition time")


transition1_value = customtkinter.CTkLabel(app, text=0.1)
transition1 = customtkinter.CTkComboBox(
    master=app,
    values=["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"],
    command=updateTransition1,
)

transition2_value = customtkinter.CTkLabel(app, text=0.1)
transition2 = customtkinter.CTkComboBox(
    master=app,
    values=["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"],
    command=updateTransition2,
)

transition3_value = customtkinter.CTkLabel(app, text=0.1)
transition3 = customtkinter.CTkComboBox(
    master=app,
    values=["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"],
    command=updateTransition3,
)


textbox1 = customtkinter.CTkLabel(
    app, height=40, width=120, text="Drop Style Here", text_color="white",bg_color="grey"
)
textbox1.drop_target_register(tkdnd.DND_FILES)
textbox1.dnd_bind("<<Drop>>", DisplayImage1)



textbox2 = customtkinter.CTkLabel(
    app, height=40, width=120, text="Drop Style Here", text_color="white",bg_color="grey"
)
textbox2.drop_target_register(tkdnd.DND_FILES)
textbox2.dnd_bind("<<Drop>>", DisplayImage2)



textbox3 = customtkinter.CTkLabel(
    app, height=40, width=120, text="Drop Style Here", text_color="white",bg_color="grey"
)
textbox3.drop_target_register(tkdnd.DND_FILES)
textbox3.dnd_bind("<<Drop>>", DisplayImage3)


textbox4 = customtkinter.CTkLabel(
    app, height=40, width=120, text="Drop Style Here", text_color="white",bg_color="grey"
)
textbox4.drop_target_register(tkdnd.DND_FILES)
textbox4.dnd_bind("<<Drop>>", DisplayImage4)

textboxInfo = customtkinter.CTkLabel(
    app,
    width=700,
    height=20,
    text="Welcome to Synthesia! Start by loading a MIDI File",
    text_color="white",
    bg_color="grey",
)
textboxInfo.place(relx=0.5, rely=0.95, anchor=CENTER)


gsButton = customtkinter.CTkButton(
    app, text="Start creating", command=generation_process
)

app.mainloop()
