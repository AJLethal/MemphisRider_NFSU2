#!/usr/bin/env python3

##    MIT License
##
##    Copyright (c) 2025 and later AJ_Lethal
##
##    Permission is hereby granted, free of charge, to any person obtaining a copy
##    of this software and associated documentation files (the "Software"), to deal
##    in the Software without restriction, including without limitation the rights
##    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##    copies of the Software, and to permit persons to whom the Software is
##    furnished to do so, subject to the following conditions:
##
##    The above copyright notice and this permission notice shall be included in all
##    copies or substantial portions of the Software.
##
##    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##    SOFTWARE.

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from idlelib.tooltip import Hovertip
import json
import os
import io
import binascii
import struct

## check for unsaved changes upon being called on opening
def unsavedChanges():
    if dirtyFlag == 1:
        confirmChanges = messagebox.askyesnocancel("Confirm exit", "You have unsaved changes, do you want to save before exiting?")
        if confirmChanges is None:
            return
        elif confirmChanges:
            saveProfile()
            root.destroy()
        else:
            root.destroy()
    else:
        root.destroy()

## "About" dialog
def aboutDlg(*args):
    aboutMsg = messagebox.showinfo("About MemphisRider",
                                   "MemphisRider v1.0 \n"
                                   "A tool to manage and export NFSU2 profile garages' data\n"
                                    "(c) 2025 and later AJ_Lethal\n\n"
                                    "Licensed under the MIT License")
## icon data
sIconData = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADG0lEQVQ4y11TTW8TVxQ9M+/NeDwTZ7Adm9hxPp04wUpsy4pLUlHFQoiqEkiAxIIFG5b8C1ZI/AAkhMQCFiBWfLQLQGpdqVWqGoppYhq3DiEf2HHixHYc23hmPI8FTmo4m/vu1btH99x3Hoc2YvFIL4BJ/I80AB6AtaOWSyZS9Y4cXLtZAnDbHxy4GJjyc+lXGebyOO8tv12d9Q4dpbJi5QofivfXl3MpAC+SiVTtgIC2o1112mYvXT1nGZ4YQDA6ht+fvzxx/soPgfDxIJd5k2XguNFff5pfevvqPxnAIQF/cOj1ucjRPhcIIXC47fAMuIWp2ASnOmwcABi6wSs2eQSA1CnhYALslfbNaqWGLlWBoRtYyaw1yzsVNh4eZYQSztT0C9VK7SyAS7F45DqAh8lEyiCxeMQJ4HJ9vzFod6l99h6V++1Zkrm9PcXpufDfzYb2en35w8ipc99ZQjNBweVx6Bsr+V8atY+LufebJgUw1+/3Xvv+4pwyHvKj225D/Mwsl02/9y0mM+vjYb+VUgLDaGFvt2pu5Xa0arlmdko4Mj0XkmZORkGFz4psahd6+11Cfq1g1qr1LdWhGtnFlca/C++09MtMWtd0N4BpAH9QAIKsWDlCyOFiXs8votloaoNjPi8VaJ4K5OdqpcYPjvloMBqwvltaDT289aM9Fo8sUAAglLQdAZS2y8itFti3p6bNzJusd2erNGmaDO17rcDkcMU37Am7PI7idn53jQKArulgJgN44J9UFjMno3XJapGnjh9jkmQhik2GyUzslfb5ltFSLJJIzl4+rd+58eA0BfAx8XRer1cbgiiJ2CmUEPrmmFIs7GJ/r4YjThVdqgJTYyhsbHOmacourxP9Ix4vAIUCeJxf2yo9vvtcBoDoiclboiR2DwX6O/0CQaSYiIwe5s168/MrJBOpMoAn7T8RYIwxXdMhWgS0HQhdMwAOsEgieJ4HYwyG0frSiW2whT8zlfs3H3W7+3oAAOViBZsb23VCeMvgmI+IkoiW0cJSapkBaHCd3bF4hAcQBTD0FfEmgG4AckdNB/DXJ1OYOeIUH7o4AAAAAElFTkSuQmCC'
lIconData = b'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'

## button icon data, icons based on Tango Desktop set
openBtnIconData = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA3WAAAN1gGQb3mcAAAD0ElEQVRIx6WVS2tdVRTHf3vvcx9NbrANgkI7SgLFWsWUDgwU4geooyY4FIuIH8CB4sB+BRUc9AOI0IHFgQOhLQFrrXYifVCtVGNI2t60zc19nHPu2Xuv5eA+cpNg29g/LNicc9b67b0e+xieosV3Tp2x1nwCxqqKMcb03/QW5VLprkp8t9uVa+fOnSt2+huAxcVFNzU1Vcvz3Oz84EH93qcnTpz46PR772OM2WYA589/y4VLF9aajcbpiYn9F8+ePetH/ROAmZmZX40x07VabdcJsvyFSqeTsrKygvc9X1UlxoiqcvLk2xRF8fKVq1e+3Gg0Pp6fn/9uaWkpbAPEGI8uLCyUBs6jdvmnHxER2p02169fH4JVlWOzszjnOHVqwY6NjU1d/eXnD4zENvDDToB1zrG+vo73HhFBVRER0jRlfHycyQOTzM3NgW4ByuUym5ubqCrT0zPu9p3bb67dWzuyCxBCUBGhKIohYGAhBIw15HnOjZs3EInDU8y+cYxut4sxhqSUYI2txBjLu2oQY9QQPDFGfIjD4DEKURRjHGPjNQ4ffmWYOoBypQrGIgrWJoBFjbPzn11Kls68FTFGEwDvPSFE1luBa8uBol8iUUOzdZCqr7D+/Z9b6RkseNhbqRJC5O8HB0r1ytxCtnZv+viHX9+4hn4xBMQYqbeEDhMcPDhJpZwMooEBw2gH665uqwBHjr7uDoseW623Xrt5t34RzOcjKQo0M+HQS/s5/uohXOKIolvD8gQN3ltjsBbz2x/33a2/6sm2GsQYyT1MVkpkRaTd8nR9ZC9KnKVWdYQowRqb7wJkQalWSr2dGIOzlr3JEKIiirfWpEOA915D8GTeMF4t94MbEvfsgLyIOAsSFRUtjKGzo00jWQH7qgnWGpwBfYb4UZS8EHwQKlUHqsQoObA5CmBQA1WDD4qMNIoqiPae9Sa8F9hHQUS39VTuA7kPmahsjE6yhBDIvVBEJXYjaREovOCjEkTQHZ2pW0MxUmRDlhVspkUWoj4arQEhBIpoaKaBNARyH1Ht7V7/o/d3yhpotrvSTouOEWkMAYBmhZC4hFY3UgiEqOxVRVTSLMQ096lamtsAaSFMTlQZqzhqzm6rwTPPgTU8eiyS5SHTaFoDgANY3fB0vbC89hjrHP9HivLgYdNkaZ6Lzx8PAKUQwu93VluzDdmXdJbrbP139yZRJE87jazTWmms3KoDJgFMu93+ZnP1/j++ouWn3zxPnOQYi+x+0X50eXnpq+bgnkqAF4ED/XQ9D0GBbn/INgBv+gFdH/Q8wQcABWLf9F8A0n+tNyUc0gAAAABJRU5ErkJggg=='
saveBtnIconData = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADdYAAA3WAZBveZwAAAWpSURBVEhLrVRbbFRFGP7mnN2z17P3W7vbbluKCDaCIF5CQgSDMcQXYkDSRHwzIKbxQas+mEoiMeFJDV7iEw+IJIiJ+iIYTaQRlbaxVKSNUOht20K37Xa7u2fP7p5znH/aEoKgPvglszN75p/v++e/DMNtePmdzg/Gi4ld2QWjzjAgL3+GxKyaRzHmQ+7Cpahr8K2jXV/+tLz1r7gl8OGxjgdP97f8kGxudTbE4qzGFMXnVGTDApstVZFbyJYXR3smy8Wy0hwaemNmsHby1KlTxvLxe0J4SeTfDSU/S67dUj89mVFGxsaU8dEReeLGDVbgFE6XG6rHa1OC6UBet3yZGdeOxqbswMY1j1/v6+szBdM9IASibds/Dgc8VmluQk86ho/YzeKBpC/z9WLJihc1vaFqmLIpK6xqGExxuVjNZPbpOcd2M1g5Pnjul+KhQ4LrrhACTZt3vB10m5NBl/aaYplnY6Zy02uOTDg9ilYoyymtYkvLdjtgmZAkGd5AhNkKw5OqrZj67sLGn3u/7y0LtrtA5GDv651n0mr1kjZb2Q6L84gtwO6AOqaHYjlnsxquawRjbHlIcOcvlvNzN7VILT8hw7yVCwk4b4CdOPreUVEINvqJuAvdtTx74fn2fS2K4uA2S+A8+OrXYfx4dUEQEyzL4sOAGVznzE7pzgN7nwmGvC6xR7g48FtDb1/PAl8KAUFm19kfLqeabmhIS62tq5FON6GxMY2GVBo+1U8mnNREtVoRawFnCLqpoL4+JWyjsRhfJxEMhsNer9rS0dERJzMhUC0yWygUgWmaqHAS8vZs75849m0PLg5Pkonw3DRqYi2wfKPT3Zdw7EwPRqdnuQNVOBwKVC/3yl5N0b4QkJi5nnvBlrysCrJzA9fwTd8IMkUGrz8Em10RuTF4BxIMbqcGw+i+Mocvui9jvqBDlmUEAkHEEwmVWVKS7JbibbFtrS2tkmHwkuYsJFIXciMRjyGabEIgWg9Z4uniwhQmk+dU1wqI8D1fKIqmhB8+j4tXmIRYNIa6uvq4ZVptQqCrq8vGa+mxcDgikQcr2LN1NVr8VWgLMyiXCljMzwkBClNFL0MrFVHjYos3R9C+tQnpuCpCy+MPu83eypj8NHFLudxMm9Ppgl2x8+sFhBeEoC+K9ifWoC2sY/5GBl5fCCYXEOCz6g9gbGgAHTtXYcPq1XAqLiiKAjvvF16J8Pn9HuKWTIb74rEEVTcWFhbgdDrh8Xhgs9kQC9Wj/ckN2NnmweTwIILhBM/XUk6GB3pweN9DWN+6Fn5fQJzRdR3lchkKF1E9qou4Je5N29r716FWq1myLKFQKCCXy4mbuN1upBKN2L3tEex/qgnDv19AgIuMDvXj/f1bsOmBjfDzmxSLRXGGyMtljd9CsVLJlMrr7FFJr1Ta4vE4j52XUZKpSqiKVg7RrSyDYcOqNDp3rcGV/vM4tLeNF0E9CotLznDn+Lkarw+TP4wuRKNRxodN0ys+duDgi6V3Dx9xUfyoD+4FEq1xklyxgqDXAZssHoE7wN92HkJK1dWrV4xPPv1IYx2vHLQ6X30T+Xx+2ejvIPJ/wp37DocDs3NZnPj8+FIf0BUp9qQ+MDCA/v5+DA5exvXr1zA+Po6pqSnMzMwgm80KR6hP5ufnRThXQkTnKcmapon1SkMu1STHiheLi4si7mRUKBTFTIeIhGzoIDlCM/UNhZUKgmb6Trg91LcECORZnHdvjD9coVCYEg8XTxrlh8iodFf65L9CWJOHREQkjfxlbG5uRiqV4i1fxwXjiEQivBz9UFVV1DsJkjgJrvynkqbYUx/Rd72sCwH54c2bnuPeRmRJYmX+BNBbU6tVUeWDZqocMfiaXloaGq91+lbSSuK7xmc6R+f1ii7CnMlkChMT45fZ7t3P7knUx0/y+C0F8H+CaZj901MzL/0FBsKxccX20U8AAAAASUVORK5CYII='
saveAsBtnIconData = b'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'
addXnameBtnIconData = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADdYAAA3WAZBveZwAAAQsSURBVEhL7VVpa1xVGH7OXWbNMksmk6VJJsk046QoFgStRVFaF6h+EvwBIuIPkILfRBCl+E0UxQUpCn6QWhCF4oo2UqQtkjSJk2iSmaa9zcyknTWz3HvP9T1nliYiCKkffYaX96zv825nLv5LOA6YA7D2VGLPZL/gxckZMPtuqBgikzYc5SpTXYvMm9q4YwJemkhCYydgO4+Q/1NEYNFyilz/AUz7kn10+v3TWSN7gjb3RXbs4aWvZmJLhzzexAGmJXxAwwFfvAX790uaYn/CTr35evWF51/0Mba/YDT22Y6LndWZdp/KtGcYnCK4eYbbjV8yuULvFxrn3NfX1w9B0Ly5ifOfvops+go8PUHc+/hzGDt8HKq3nwro7BG612KwQj6GABQUqcqXaKEORWmoDX6gP5ePJ9Tjjx175eiDD0mCnz88iYjfQHRYQ7gPuLG+DJv1QA+OYWtrC8ViEalUCpZlwe12Y25uDi4Xh8JKUJUtKE6KipImB3QY+Zj+9TktorXcaGH9t28w9dRhCtst52upRXiMP9Eb30Emk8H29jYajQbq9brcT6fTZHiAnAthapxhIGxCVfvA2QwsJ6JZ/NewIk+2wTQNnLyzLQ7HtsEdTuJIbyORCIaHhxGPx+XY5XJhdnYW4YFJ9PTeT8V4Ag3+NOrWkzDtByiKcWmzS7C2fhFldwCrK1exsZbB6moGWzsOjGIO5YqB0dFRTExMYGRkBKFQiPKsyHk4HMbQ0DRU7SBMK0nGp2Dz/rbVXQTnvnsbaV7DhZUV/HR5Hj9eXsBSoYiL6xcwf+VbNJtNWYNSqYRyudzVlUpF6mq1CtM0ZfFFE3TQJVhY+B7qQBbVaS/y0z7kJ9yohSswbs5jc3MJuq7L1HRkcHBwjwSDQXmm02UddAmOHHkWecNE+o8CjEwF+Rs1FPIN9PpjiEaTMoJCoYBsNis7arcWe8JzITbVbjcBe+PUa87Jl16mMEt0wEZ15xYdsOWm20UtqnupS5SuZx3ppOLvYyGiAYrFAs6c/fx2BNeuXacND8olE35fBPWaAsPI0cFWrg3DkIZEa4o3o6oqllMLlPcm1jdWpYPXjU3ktrOSpIMugVgURRKXhSFRtFKpLMMXD6tWq8kzYr0DzsljoYXn7Z+4K6SDLkEH0WhUFmt8fBzJZFIWNBAIyJbU6J0kEgnpvZBDyXvg9/txMH4XFVm0rkqetg210SUQj0j0tjAiLos8ejweSSbWxGMT2uv1dgl8Ph9cuotS6ofP68NkbAqx2KQk7YC9895b50PB8FEuqy9WWht3CuqmcqVaXmYffPzuo7lsfszhre8B5VsVQvXQmqap01izpLY1uiT/u8h7S9NIdN2kqCwXaYqU1jRbiDhD88ZAKJD7J38pkTJ1QguDQu8eCwgjQsTXa7cWcrvC/+PfAfwFfN8ubfJ/ddoAAAAASUVORK5CYII='
aboutBtnIconData = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAGF0lEQVRIx42WXWwcVxXHf/djZvbD3rW99tpefyW14zgfTRORh0KLEKSQIqpWRe0DSDwhhQcewhMSQmrUh1IQb6hS1UrwgiJVCEpRURXRGqiaxkqatM2HY5J6N3GStb2Ovfba3o/ZOzOXh7UTELTKlf6auXc053fOuWfOHcGDjBMn5PD5WFoos0M39Eb+bz/Lg7AP8qr4vAcjT700QSieRfAEMCGg04IRILBIENcsnEZFr3bnuvMXXv+ReSDAl4695iwXV38souiHA33psYfH+t39o71i13C32DnQBcDVwhLT+QV77sod/2phqdo04csIdXLunZ8ufiFg8Fu/GNOKV11P7X/uyIHMk4/tdoIgYrpQ4ubCGsWlClJIxkd6GB/OcHjvAFMX5+zv3vpo9U6pcj7C/vrG4o33ufC6+R/A3udPuLWq987OgcyjP/n+Y3EQ8r1zeS7NLhJEIJUEBAKLALSWZDuSPPO1PQz1tts3Tl2qTV269e5Sef2VW6d+PrltV23fJEaOHvc859kXjh1J54tl+ed/zlBc3gChcF2F4zjsGUiz2bQ4jkIIyWa9yWe3V4gs4quHdjiVzXrv7btrlfaRI7OV/OTaPcDIUy9NCCte/t6TBwcHsmn91j9mKG/4uJ5LzHPxXIffHH+CHzx9mH3DHZyeXkBJiVQKYyIWy5uMDWZEtivpNfygr3h31e8e3Xe+PHsulACEfHco1zF69CvjzuS5PKvVJvG4S8xziHkOibiHVK1glVIk4x6JuEfM0ziuxg8izk4XyXal5KHdA4OD2c7DociNA+jWRohvPjKec30TMl24S8xz8La8dxyF4yh++cZ5hjJJiuU6ibhHFEaYQNGQBhNI5krrVKo+2Uy7MzqUGby9sL4PuKx5/g+KzdmJA2N9YjpfwgqBo3UrNZ7egmiOfXsv2a42CvNl/vjBDYwJkEqy/bUFQcRiuUYuk1CD2XSvkHYcQObKsx0I0TE+0iPmFtdwHN2SVriOxtWamKvp624nl03R29VOPO6RSMTwPOeeA1IJ1qs+nqvpSicyCLsLQHoxOWqxzZ0DXSwsb6J0KyVKSRyt8WIaL+YiRKuipZLEYq3UubrliOMopBBsNAK01qSTsSSWXgAdBFSVQgghEFIghURKiZQCKQVKShxH3wMIIYm5GoElDCNMIFFSorXC1apVXVKEQogmgLz9aH0Gi565scT4UDdgQYBSEqVaMCUlbEewVZ7WCoTYmktJzHPpzbQRRRGVaqMshZgFkLz4YmTh+rUbJTs2lEGJFsNaCMOIMGqJre20NiKKIoRorYRRRBhGJOIu2c4ETWPs8lptIQjspRYAQMjTZ6fvmMN7B0gnPYIgILK2pcgSmABrW4AoijAmoGkMxgREUUTM03Smk4z0pqjXmsH07OIC2s7cB8jwlY+m71SvzC7ao18eI+Yomr6haQKMCWj4zfuAMKJa9/F9gzERSkpS7QkOjWXxfWOvFBaXr99c+cQJkh/fA3TnuvPNhvnVa2+eXds11Gkf2dWHkmBMgO8bGr7BRvcjqNV8Gr5BSUGqPc6OvjSj/SmmPimYqYtzb1dN/eTsqeP+vV60cOGvUWr064XNmv+4taL38UM79GA2Jap1w3qtiZKCDy4VeXsqz8fXl9BaEfdcOjuSHBzt4cDODGc+LZgzn85NForLv4/FGhfuXn0//K9uWsn/fbN99BultfV6z9pmLZvrSXl7dvaIwWyKZKzVl7RWtCU9hrJpHhro4MBDGTSRfXfqmjlzcW6yWNr4bdPUP5x584XNbbv6Pw+c7lJmsticlyvLK3PrG/XvHJwYzPV1p3Quk5Ceq9Fao5QgDCx137eFucXo8vX5tdPnZ96bn1/8S1AtnS2eO7n2RUemC7SnR4883Na/77nhof6Du3b09Q73ZTq7M+lkqj3uCmtZWV2vz5dWKlc/u1W+np/71/Kti3+ql65cNdW1FaAC1IDo/wHagBSQ1rHOTLJ//4ST6t/tJDqGldfWL6SXgtCGfqXsbyzPmfXSzer8hcths75teB1YBTaB4PP+KjTgAXEguQXdvsa3Kq++ZWRbtS01tg1vj38DwkCcCvji0AkAAAAASUVORK5CYII=Y29tL3hhcC8xLjAvIgogICB4bXBNTTpEb2N1bWVudElEPSJnaW1wOmRvY2lkOmdpbXA6OTlkYTRjMGItN2UwNS00MGZkLWFhNjItZThhMzk4YjNlYmM0IgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOmY2ZmIzY2FjLWRmODEtNDk0YS1iN2RjLWJmZjBlNDIwOGI2OSIKICAgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjUwYmM3MTFlLTFlMDItNDg4My05NmU3LWI3NjQ2NTc3YjRkNyIKICAgZGM6Rm9ybWF0PSJpbWFnZS9wbmciCiAgIEdJTVA6QVBJPSIyLjAiCiAgIEdJTVA6UGxhdGZvcm09IldpbmRvd3MiCiAgIEdJTVA6VGltZVN0YW1wPSIxNzQyNTg4MjI3MDQ2ODk0IgogICBHSU1QOlZlcnNpb249IjIuMTAuMzgiCiAgIHRpZmY6T3JpZW50YXRpb249IjEiCiAgIHhtcDpDcmVhdG9yVG9vbD0iR0lNUCAyLjEwIgogICB4bXA6TWV0YWRhdGFEYXRlPSIyMDI1OjAzOjIxVDE0OjE2OjU4LTA2OjAwIgogICB4bXA6TW9kaWZ5RGF0ZT0iMjAyNTowMzoyMVQxNDoxNjo1OC0wNjowMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmZmM2FkOGExLTdlODctNGRiYS1hNjQ4LWViOThmMmY2MmRmNyIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyNS0wMy0yMVQxNDoxNzowNyIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz5aOuJXAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH6QMVFBEHC2qAiAAACEBJREFUWMPNl3twVNUdxz/ncXc3m2TzDkgC5gEUQtRECKKUIT5QBNuirfSPjuNox3HqjHZ0pnY61U6q1alO/aftOBW1aGu1yGh1FMpTUEYBxSCPyCMJBCSQB5uEPPaVvef0j3t3JZYZqdOZ9s6cvXf37jm/7/l+f68D/+NLXOwfm5tb9PFcZ5FA3C4QiyyUAgX+63MCzgrsDhe7tnpsfMf27S3p/wqAqhUthSIZfATBPdOnlXFdU21+U/1UMbk0n5JIDgADw3F6oiPsaTtlt37SOdLe1QeW520w+Zuut1qGvjGAqqVPPiCVeHzpwlk59/5ggTNzWulFcdbxRZRVb+weX/fB53Fj5aNd63/++/8IQFVzS8iGQ3+bUzvppsfvuzG3rrochLfwh/tOsvfIGaLDMQbOJRACSgtzKCnIpXHmJVxz+VRqKosBONLVz6PPbh470NGzkbH4j7q2tyS+FsCc21sCY2PBj1dcWz/7V/deH8gJOLR/EeWFt/fw6aHTaEehpEQIb2rmDmCsxRrDvNkV3Lm8gdrKYhKpNE88/17qja0HDoXDiflta1tS59tTE81bkVe9680V19UvePL+m4KOVry1/XMee3EbfYNxAgGN42iUUmilkEr6z9J7lhJHK85ER9m0u5P8cJC66jKua6pVvYNjRfuOnr1y6OiWNfDrCwOoXhb62dUNVXc/8+DyHKUkf1izk1c27MdxNFprtFYoKdBKobVi+bxKll9dQ3kkwPG+MaSUCAlSChCCPYdOMxpLMXf2FBY1VuuDnb1TRyPrUoNHt3z0bwAqbn2yJEc5a5575LZIcSTM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'
slotExportIconData = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADjklEQVQ4y9WUW2xURRiAv3Ppbm+02miJlF6wNPRGwdZbi7UUKJfGaFtIY2LAJxJtkEQk+uClvmAUWUIIVEMwBjUhhoSAAmnaFSzY1lsUsKlZ0rRU2c3uJghnu7une87ZMz4sbLNYElN88U8mk5n555v/Nj/830S6V4C4vhiUGKSBlPXnfwMW0SJABluAJCVo0zJS3ngq+P3du74HnpjjOz+80XXoSWSBlPnHDPiD3e/9nJ8/v7btuY45eXHi5HERDAZ+ef3lQ4+SbaEm3ULUbdrYiaZpeL3elEv+v3wMjPbyW/AcEWscRZ5HlrqQdUs201DRREFBAZs2dkoHP9pfhwxElRkwgGmaBAIBVHVme3j0PF9eeoeiooU0tyylsGQtoZtTeH1eTg3vYXDiDNvWdFNTtSxpopQ1iZxSIpKEoijJ8fWPxzg28i7rn22kraOVvIdhRD/BhKMXZ1mQLVvbsTLG+fxCD5J0K4IigfwHWFVVVFUlFNXoG3ORe18O7tM/0XPgMy5+d5XKnLWARMj044n20dbeypUbvUz6JhKM7MSszgYGODJwABCk6cXsWLMTwzLYf3Y7zjQHRXWV+KZH0M0wobRrFC96iI9P76GEqiTrrhZPar+SoRSy64XDVCyqZllZLa8072Pk8jjzWEAsGsfQ4/hujlFaUsY1zZOS8LtaXJhbTX1pC+nO9OR5bfnj6N9cR53OwYja2LZNXNygND2HiHkpFbx334cHDcPouhP8SNEKHquoT6mQZGnaCoZuE4/HMTFw3p+JaU/d/mTC4XD0qIZhdG3f9iq2bSOESGa3vel5ZEnGc3WUt45vSAHLQiEWsbBtgRAGzgczsEWErwLdt1W6ZADDMNA0jVAoNHNZSoR/SUklO1q+QJYyaWxYyYudL2EagljUIhaNE4uYiLjMlvYu1jd2oMhZLM/enIhxLBZDlmWEELN+1/qljYSjLj4Z3omzIYsr2hCWMaP77dhRqvKacQ/2sfWpvfg8/gT40yOH/1U/KHE0MTDkpqWplYvBPgxLx6FmUP3ASvrPn6HYsQqfxz9723y7+82CcHhKUWRlATAfify4FZdNy1otAaNp7uW2w7+4ecVq6XLwLDX5qzg36LZjhj445LKevqd+3PCaOpKdkVvR0viM3H/hlB3Wtd+HXFZ1SoLn2HtrwrrmPdl/lLCueYGaOxXmBB5yWTZQbgu7Hyi/tU6RvwGCiW4Z2KCRQQAAAABJRU5ErkJggg=='
slotImportIconData = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADcElEQVQ4y9WVf2jUZRzHX8/z/d7pbvNcm5u1o1hlkUEG6jh3Yo3KAom0NjYsIigGa0lliwKjJKRIZW2FUqxkZv5jwTB0C2lbuubW4VaeKepWcz+6xZ1b7W632+573/s+/XHs5JjJWP3TA58/Hp738/o874fn83ng/zbEvwWo8RWgxcAGInPkvwGr6G2ABEuBEEnajETkDKSDP9jz3o+Ae4F5vG9WN6xDKoRj+Bp49573e/Lzl6/esvmpBbk4+k2TCgYDP73xYsNaskz0lC3UmrLSckKhEH6/P92yUgAkLJNjZ77iiaIKNC21FZfLRVlpudj/ycdrkEBUuwYGiMfjBAIBdF2fe59Ksa9lF4Ph7/g99BuvbnoXIZLmAoEADocjdUSROYRMeyJCoGnadeNAWz1jcR+bN25lLO7jQFt92vpsElQSOQes6/qcONLRSH+oFY+7CK//KB53Ef2hVo78cDClmQWLrCvzAzd7m+j2H6LEs4FzwXYMc5pzwXZKPBvoHjlIs7cpDTw7bgju8LXSfKmWh9dv5PzYSQxzGgDDnOb82EkeKH6Q45dq6fC1zh/ce9nLlz07eGT9Y+Tl3EzJiq0ICVIX6HbBQyufxlVwK551RRw6s4PTP59KL+kP6/fuNwyjGmBb9StMTEwAUF5XmCZ8rqyKtsFGhFBIKXj0rko+O7wvTVO8tIq8xbdgs+mf6oZhVL+8bTuWZaGUSln6+rWh1IaKupXEzGkyMu1YxNE0DUsk0nROpxMhBFf/CrKzYXuVDmAYBlNTU/9YVbrIIhaPkpFhxxQWUkqETIItKzkPh8MAdJ3t4Gp8IHnHsVgsKRbiuuGw5RGZCZPtvIlFDg27Q2IuDuOwL+NsX29KZymLxs5dRBKjycpr/OLzG/YBK6H4dfAy7jvv4Up0HKkJJhnl3lWF7G55lrWdz6AJHV+khWhimGx91dy2+fbOt1yRyKSmSa0AWI4gfzQxcP+Q+Palysrn6YufIGZNIZDct3QTXad6rYsX+kApnNlL+HN8QoJaPe9O5nld71+Wm3NHacWTcjDWzWQ8gCZs3J7pJtdeSN/ARU4cb1cJZbac3ms+Pn9wjX43gk67vijX4ymWrgIXzuwljAz+wS8XfNbw8JBQqLquWrNmQT+Ip0b/CMELQAYKCcwAPcA7XbXm97O6vwHpzFBss4CGCwAAAABJRU5ErkJggg=='
slotClearIconData = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADkklEQVQ4y9WVbWhbZRTHf/e593Zb09Y225LOjHXtqrPIHFvtVOhGnTJQaBVXhuIHYVSwdSh+qH4QX0Aqs2ObimUwhlW3L4JMnS9oVVSk1Na1Ol3s2q4LfQkuSe2aNLnNzc29jx9C08WuDKtfPHA+PYffOf8/nPPA/y2UfwuQf1aCaoIOimvivwFLYwMgwJGgKBlaUqC4L+WCD7a3/Qjcscw+vc+1HL8TIVHyxxfAr7W/etbj8W5/8IGHlqXio49Py3A4NPBs8/HbKUijZWUhqxv37iMajRIMBolOhTn3WSdp02Br/eO4S30L/im5vX0+H4179ykdx96sRgCGiri6wLIsQqEQmqZx9vRb+OQXVOb/QN+pF5mdDqPrOrquo2laToZCISzLyo6ouMZywYqioKoqqqpimwkKVgk8xTpV3gDnPj+JKgSRyT6Q6WzdfGZVyAxyEXh+im0NTzAUqcSyJaXuPJzZAIO9HUwONyOltWjqebBSEABY8PhqMMCmLdUY0f30fvs2W9aP4K3qx+uBhGsnOFa2binflwQDbL/7fgrdRQRHmtlWU8eG8h30vNHFxa6j6Pd4WLt+Nx7fbWj6ykXgJa3QNI0rkVHCk4eprdtDWdlmRo9+jfnBRbY2rmFnbREu8T793zxKYPBTUmYiV8GR1w91pFKpFoADLU8zMzOTfQwF/VzoP0ypO4nzXhh7OsGud+5lhVuAsgrUEqy0C7+/m9/9E8TNCgy7AiXPc0w52N4mnzrwDI7jIKUkFovldHYcm5/aXobAd9Sf3I8Qf4C6DuwQ2EGcdIykU04y5WZy8jwTE3OELk9mPE6lUiQSiWtulBAqGx97mHhkHKHngRUHOQpOFOwwSWOaeOI8CSPJ2pK7WL36Jr76MpgBm6aJEAIp5TXhJd6NDP8yheMoKNYoUlpYqSRJM86cEcUwZpBSIrRCJsb8WFRlwJ3vnrjuLVijrmR8/DeKXfmkjF9JWyamaeA4aQDyS+7DmBMMDgaI2bsXn80XXnreF4/PqqpQbwS8KHjstC2KVlx+5Nby3tpddfVqPHIKx57NWKW5cZXs4UrUkn09H86m01ZDUyvf/6NL1nmE7ps376ip2FSlJ2M95OXfgtDLuDTSnR4aGog4DnVNrQwvWpDrhW3TMHSh7+fConW+G4prxNiY3xoZ6Uo7dvITx+HJplamlv2DnDhEmaIwoChI4Izj8EpTK4G/1/0F+xB8831SyvgAAAAASUVORK5CYII='
moveSlotUpIconData = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAL/SURBVDiNtZRNaFxVFMd/5368eZkxRmQsbTEGxbZC0IWMpU5SbCmxILapFCO2LgSlWbhLbFJBcKErP0BcCIqCdeEiUAviQoJIwIgW3biwCoYGjTImTIXWTjsz7+O4yLzwUkuSgjlwuPdd7vmd/z33vCuqymaY2RTqZoLdRjfunXTvg2zfNh8PT01p8r+AByf9S9vv6DuGQWr627vA6Hox65ZiYMIdva1Ufvlg9WhpaM+RYs+t5eN7J4IX1ouTtbpicCyoFEulmacOniidr8+SpBG7ynv4dPrjxpVW48i3b0Rf3rTiR8al13o3/cSBZ0uLV+f46/IFapfmWLh8nsf2PVnyzp0ZnAx33RR4cFK6U2dnDu97pie1LS5c/BFnHNZ4fl36nkZSZ6h6qBuNv6qOye0bAo+MiFXc54/uHundUt5qfln6Dmt8xx2I8MPCF5RuKcrAg0NbjHfTlVHx64Jrd9v3qv1Du/t3VPxPta+xYvHOUwgCfGBQ28Z45dzCWfruvMfdf+9D/V099vSa4IEX/fh9d1WO7a8Mhz/XZjFOCMMCYVggCD2RaeAKQlAw4CPO/XmGygMPh33bdg5XJ/ypPGulK6rj7vG+rTumnjt0qss5j5KikjAzf5pYWtSvzXMt+Wc5SuHwzpNoqmgKzXaLs9OfXK1f/OPp2bfizyD3gxgr478vznW98sHzAFgvzVdPfBj6wNFoLxLZBt4bBFAF44R3PnqtGbc17CCKOBkDVoNnX4/2X1cWNdbiA8+V1hK+YDAGEEFVsVaI2xp+82Yk19d3FfhGZozQiP9GbYwLBOMEEUFTRewNeRsEi6WZXkIMGCs4bzBOiNspsjZ3dVfIsjkRKWRrzbgBCppCmihJpGgC6EpMUUQKIrJKpMuAgO98u84cVTjQO4pKirEgIizfHqTpyhvTDcRAJCJxNne5BDYHdUD95NvHy2sfmHomImcKJKKqmeI8NBuzZKbjHb2kHY+BJFMJtIG2qqb/eTY7SWzOM6jtbElz8CQHV83B/gXtSQriGSyg6AAAAABJRU5ErkJggg=='
moveSlotDownIconData = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAL8SURBVDiNtZRPbBRVHMc/781Md1bTGMCkhYNtOIiAnkw0bSFpNCGeOEAwMRyMMaReNCY0JXpFozQWT3JWExsEIzaxJkSREGiJIglRNCqVDSEIxlKqsN3ZeX9+HnZ2O112Wznwkl/e78283+f33nd+v1Eiwv0Y+r5QgbDdi4GR6AaermWjNX9NjZruewLj6Xp76COsNzhvsT7FeYvzBusNqUs4dPittonbgwFQnP7jCFW7QNUukLqk4T+3cc8Kl7nHoVD/a98KYEFYrBqR2lrEs1I1LQtehHgEX3signHVFU/c0HjLSHRSPIONjKFKRHws4vF4vNQsdRUSW27sGRiOFo+uOTU1agaXgL2TsZ7uR5/es/3NYhhEOLGx8xYvFrRHh4L3CQm3iAoaHcAru96IRcCYKhMnxhdmb/15sM5Tea0GhqO9m9Y/uX/H4MvFC9e+oWLnsVSp+jvMVa+R2H9BAQIiEOtOtvbs5uTUVwuXr8/snx4177bUeOo9M/brlR/Gvz13LNm8rp8gVBhV5u/qDFbfIYo1HbEmijXFYszW9bs4f/FscuXGpYk89C4wwNqSG5r+5evvf7z0ndm4tp/ZtITq8EQZMIoDOuKAvp4dlK5etj/9fu7nyrx7sZmjWpXNln2qU6nowvZnX+gNH6roi/PHCUKNDhVKweOrtlGZ0zIxefS6M/aJ6YMy18xoWW5nDshtbczg5Imj/xTcKjas6SfsUEQFzYaH+yi61Xx5/IvbQvBMK2hbMMCpMblqU7vt2OSn5e5oE+sefKxmhc0c/ny8XE3NzjMHkt/axbeUIj8GRsKdqzvXfLz7+ZceCCLFJ599WL45e3Pf6dH0g+XiloCVUgoIcqYB3fdasPeR3t7hoKBUaaZ05Oz77nXA58wBTkTsEnAGjKg1TJjzg2zWT70avBMEuuv8ITOUppgMaDOoBUw2W8DUwVEO2Ow3r00OYtqs03pL16/Q/E+sX1NnlvVdQ4LmE6dAKiL+ro/XTufMryerw10OLpKD/QceAIZcIO5IFQAAAABJRU5ErkJggg=='
exportPresetIconData = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADf0lEQVQ4y7WUf2iUdRzHX8/3nu2msmudczjxuGM2MleL6KyWONtmLgu3nURIvyiHxiQoMBDUsEKi/hGCAuGe2qo/CqScINfcplN0O+iPEZvr0pRd4uy6Dbe7tvv5PM+3P7a77XaKBO4DHz5fvt/n+/68n8/n830rUkqWwgRLZEsGrHZ0dBzXdX3PfUxiqqrqxev1GvI+m9frNdQM02AwiKIo2bSZ9eK4eJ1pfiY6HA4AoS78eGJigkQikQcSngxxIdDF5fE+ZvRRLMJGiXUdr2xso97dmAOcrXG2i0JgsVgQQuQA/3rlEieGP8bpdFD3fDUOVyPRqX8ZuzXGt/5DdA2d4MNdx7CteCAHXCwELisrw+l04nQ6cblcDPzZx8nAp2xvrqVl54vYK+ByvJPRwi6slWHe2NNErCDAl6c+QwiBECKfsaIo+Hy+7MF0MspPo0dYubKU7tP9nLUM8vCGtTxTu43hiI9oOsQVo5tmzwt4vd9wI7QPZ7krn3Hm91tbd9PaupsbegCQ2MxqGla/x+Ed3xMY+pvBgQDlRRsAiKeniXITV4UD7cyxHMY5pZhNIIhEphj55xLLVRcdB05TXuzgiUfcHGzWGBkOUswakjGDVNzg1tQ1HnKtZyxyNac36p1GqKTETmWpm4bHm1BVNZt4Y9XTxE6OoyZspGImpmliyEnWFdmIpPrvXmMATdMAMOIKwT/+QhvVssCZi9K0kIqbGIZBmhTWB5cjZeLujD0eD+8fPjK3U8zgzSAxdZyQ9WfaP2qbr5+0kJzRMU2JlCmsq5Yh0Xnp6Ko7AyuKgrWoKGfQrTjY29LJ0VOvs6nGTcXa9aRTkmRMxzRBmhJpCN707CM8EaK3v4ea0rfygdWCwjxV2eJuYDp+nC962rA+u4KrkQH01PxjOH/tB6rsdfT297B/u0b4+u154Az454cOZF9fJiqKwo4tHqIzU3znP8jW2gZ+C3eT0uMUqst4tPQ5ei+e5bWnPqGpbifadQ0VMAFht9vvqYdvt7xDZGYSn/8rNtfUMxQ+R3VZPRf8fpoe28/el9/NSqfS3t7+v/W4O/gjUWWErZsb6b14BpusYptrV1bwhBBfKxnhUGZnRZ3zAqBwgVvn9hRAt67GePJVtU8IscaU5ljgF6Nq8neZBNJSSiNnKuRshvScx+/FetMHBZWmNDuBltsjZmzx+X9EYa7x+4yIYAAAAABJRU5ErkJggg=='
importPresetIconData = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADV0lEQVQ4y7WVXWgcVRTHf/fuzGyW7LabLcaYGIi2AVNQwYeG3cRQYyJalJJoaOuL0iDaNy0VEUNiUASLxfqBTdnFhLYSKSKCzSKhNkmTWNRiU220WGu2iTHpstJsU7tfszM+pDNmuxtQaA4czh048zv/OefeO8I0TVbDJKtkqwZW+vr6enRdf+4WFjEURQkSDAaz5i22YDCYVSylkUgEIYRd1lrfHG9eW8O3YmVlJYBUlifHYjGSyeSKkKyR5djpo2xreJaysjsKgvOGJ6XE4XAgpSzoQgoOHH+L8T8Osn+gGyEEQojcnGUilOXg0tJSW6Xl1vPe/i6uZCfZ2ryDE2ND7Dvazcvbu221Qogc1TmtCIfDBcd8cmaAef07HgzU8u3sF/hrGxka76ftjRHcsxsB6Dt4YGUwQHv7zhzooS9DTF/4muaGR5mIDpLWE/wYPcHDdY8wODJA+s61lMRrcr4wr8dLBSTx+ALx+AKfhg/z8dirNNU/xrnYMGk9AUBaT3AuNszmQDMJ5wQJ33xej2Wh6Xu9PiYunKFn5CWa6pq4zVfG5g07EBKkIlA0QWPN01SUV1Lvr+eKY5i9oTdtcQVbEQqFAOg9vwuAr0Y/B+CZp17AWawihImUAlUTBI/02KDR6AdsnWrFX1KPaZq54JaWFl7s6ALgbp63X4q4j5DSE7iKNQwyOBwODJEFYKDjMl6vj1AoxMb19zIfm+OH6GguWAiBs6gob1eocg2pzHVcLg1dGDf29RLY7fFgmoY9p1Nnx5hNnM8HK6qWB3art3MteRXvuhIWs1GEFOhFV3GqHl5/t4Mqb7V9MnuOd5LKLvwLtuBvv/aKPWEr7vlohouXvmfT+mqmrv+FdAgW+ZP77q/hmzP9bGn8BE3V2PV+G9cyv1HqrEUBDED6fL4V78HdbV3s/HATTY0P4VInSRl/M5f8mQcCW0jrGTo/2w4meLxOQNBQ3mqI3t7e/3Qfh6cOYXgu0rrtCSKpUyxmLuMQKncV17JOq+LX339h8NhJqt2P469oDgnrGIql/abccBXQlrnzniflBl+VPKypzrWBgF9WlFewxuthJjLHT5NnjenpS8I0zf3j+zK7AcT//ZnW7VHfQ9AOuDCRQBI4DXSOv5MZsvL+AWGthETiHqtEAAAAAElFTkSuQmCC'

## defines main window, frames and their weights
root = tk.Tk()
root.title("MemphisRider for NFSU2")
root.protocol('WM_DELETE_WINDOW', unsavedChanges)
root.minsize(300,450)
smallIcon = tk.PhotoImage(data=sIconData)
largeIcon = tk.PhotoImage(data=lIconData)
root.iconphoto(False, largeIcon, smallIcon)

mainFrame = ttk.Frame(root, padding=(5,10,5,10))
mainFrame.grid(row = 0, column = 0, sticky="NSEW")
topFrame = ttk.Frame(mainFrame, padding=(5,0,5,10))
topFrame.grid(row = 0, column = 0, sticky="NSEW")
mainNotebook = ttk.Notebook(mainFrame)
mainNotebook.grid(row = 1, column = 0, sticky='NSEW')
myCarsTab = ttk.Frame(mainNotebook, padding=(5,10,5,10))
myCarsTab.grid(row = 0, column = 0, sticky='NSEW')
myCarsTabLeft = ttk.Frame(myCarsTab, padding=(5,10,5,10))
myCarsTabLeft.grid(row = 0, column = 0, sticky='NSEW')
myCarsTabRight = ttk.Frame(myCarsTab, padding=(5,10,5,10))
myCarsTabRight.grid(row = 0, column = 2, sticky='NSEW')
careerTab = ttk.Frame(mainNotebook, padding=(5,10,5,10))
careerTab.grid(row = 0, column = 0, sticky='NSEW')
careerTabLeft = ttk.Frame(careerTab, padding=(5,10,5,10))
careerTabLeft.grid(row = 0, column = 0, sticky='NSEW')
careerTabRight = ttk.Frame(careerTab, padding=(5,10,5,10))
careerTabRight.grid(row = 0, column = 2, sticky='NSEW')
bottomFrame = ttk.Frame(mainFrame, padding=(0,5,0,0))
bottomFrame.grid(row = 2, column = 0, sticky="NSEW")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(1, weight=1)
topFrame.columnconfigure(0, weight=0)
topFrame.columnconfigure(1, weight=0)
topFrame.columnconfigure(2, weight=0)
topFrame.columnconfigure(3, weight=1)
topFrame.rowconfigure(0, weight=0)
mainNotebook.columnconfigure(0, weight=1)
mainNotebook.rowconfigure(0, weight=1)
myCarsTab.columnconfigure(0, weight=1)
myCarsTab.rowconfigure(0, weight=1)
myCarsTabLeft.columnconfigure(0, weight=1)
myCarsTabLeft.rowconfigure(0, weight=1)
myCarsTabRight.columnconfigure(0, weight=1)
careerTab.columnconfigure(0, weight=1)
careerTab.rowconfigure(0, weight=1)
careerTabLeft.columnconfigure(0, weight=1)
careerTabLeft.rowconfigure(0, weight=1)
careerTabRight.columnconfigure(0, weight=1)
bottomFrame.columnconfigure(0, weight=1)

## adds tabs to mainNotebook
mainNotebook.add(myCarsTab, text = "My Cars Garage")
mainNotebook.add(careerTab, text = "Career Garage")

## loads button icon data for use
openBtnIcon = tk.PhotoImage(data=openBtnIconData)
saveBtnIcon = tk.PhotoImage(data=saveBtnIconData)
saveAsBtnIcon = tk.PhotoImage(data=saveAsBtnIconData)
addXnameBtnIcon = tk.PhotoImage(data=addXnameBtnIconData)
aboutBtnIcon = tk.PhotoImage(data=aboutBtnIconData)
slotExportIcon = tk.PhotoImage(data=slotExportIconData)
slotImportIcon = tk.PhotoImage(data=slotImportIconData)
slotClearIcon = tk.PhotoImage(data=slotClearIconData)
moveSlotUpIcon = tk.PhotoImage(data=moveSlotUpIconData)
moveSlotDownIcon = tk.PhotoImage(data=moveSlotDownIconData)
exportPresetIcon = tk.PhotoImage(data=exportPresetIconData)
importPresetIcon = tk.PhotoImage(data=importPresetIconData)

## defines tab button style
tabButton = ttk.Style()
tabButton.configure('TabButton.TButton', anchor='w')

## initializing main variables
dirtyFlag = 0

xnames = {
            "PEUGOT":"0x13E5B272",
            "FOCUS": "0xDF04CA02",
            "COROLLA":"0xEB137CF7",
            "240SX":"0x80FB5001",
            "MIATA":"0x6B5D4503",
            "CIVIC":"0x4DC09002",
            "PEUGOT106":"0x0A07104B",
            "CORSA":"0xD7FA9302",
            "HUMMER":"0x4DDD2661",
            "NAVIGATOR":"0x4AC91902",
            "ESCALADE":"0x714770CF",
            "TIBURON":"0x2205FD04",
            "SENTRA":"0xECBFAE79",
            "CELICA":"0x60EC5A54",
            "IS300":"0xEE360203",
            "SUPRA":"0x8AC4B803",
            "GOLF":"0x87301600",
            "A3":"0x53040000",
            "RSX":"0x7CDB0000",
            "ECLIPSE":"0x84DA0275",
            "TT":"0xE7060000",
            "RX8":"0x01DC0000",
            "350Z":"0xD1C60A00",
            "G35":"0x6EA80000",
            "3000GT":"0x5D9B7C2D",
            "GTO":"0xC9AC0000",
            "MUSTANGGT":"0x19581635",
            "SKYLINE":"0x5E3748BE",
            "LANCEREVO8":"0xF6EFD209",
            "RX7":"0x00DC0000",
            "IMPREZAWRX":"0xF85844CF",
            "(empty)": "0x00000000"
          }

userXnames = {}

def loadUserXnames():
    global userXnames
                            
    if os.path.isfile("userXnames.txt") == True:
        with open ("userXnames.txt", 'r') as userXnamesFile:
            userXnames = json.load(userXnamesFile, parse_int=True)
            userXnamesFile.close()
    else:
        pass

loadUserXnames()

myCarsSlots = []
for i in range(20):
    myCarsSlots.append(list())
    myCarsSlots[i].append(0)
    myCarsSlots[i].append(0)
    myCarsSlots[i].append(0)

careerSlots = []
for i in range(20):
    careerSlots.append(list())
    careerSlots[i].append(0)
    careerSlots[i].append(0)
    careerSlots[i].append(0)
    careerSlots[i].append(0)
    
openProfilePath = ''
openProfilePathPrev = ''

myCarsSlotsList = []
myCarsSlotsListVar = tk.StringVar()
selectedMyCarsSlot = 0
firstFoundMyCarsID = 0

careerSlotsList = []
careerSlotsListVar = tk.StringVar()
selectedCareerSlot = 0
firstFoundCareerID = 0

newXname = tk.StringVar()
newXnameHash = tk.StringVar()

filePathStr = tk.StringVar()

activeList = 0

presetImportFlag = 0

## functions to validate characters inputted in text boxes
def inputCallback(string, newString):
    spChars = ['', '_']
    if len(newString) > 32:
            return False
    if len(string) > 32:
            return False

    for i in str(string):
        if i.isalnum():
            return True
        elif i in spChars:
            return True
        else:
            return False

def inputCallbackHex(string, newString):
    acceptedChars = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','A','B','C','D','E','F','x','']
    if len(newString) > 10:
            return False
    if len(string) > 10:
            return False
        
    for i in str(string):
        if not i in acceptedChars:
            return False
        else:
            return True

## sets fileLabel to active file
def openFileLabel():
    fileLabel['textvariable'] = filePathStr
    if len(f'File: {openProfilePath}') < 72:
        filePathStr.set(f'File: {openProfilePath}')
    else:
        longpath1= os.path.splitdrive(openProfilePath)
        longpath2= os.path.split(longpath1[1])
        longpath3= os.path.split(longpath2[0])
        longpath4= os.path.split(longpath3[0])
        filePathStr.set(f'File: {longpath1[0]}\\...\\{longpath4[1]}\\{longpath3[1]}\\{longpath2[1]}')

## checks XNAME hashes passed through it against the built-in XNAME list and the user XNAME list, then returns the result
def checkSlotXname(slot):
    slotXnameHashTmp = binascii.hexlify(slot)
    slotXnameCheck = str('0x' + slotXnameHashTmp.decode().upper())
    if slotXnameCheck in xnames.values() or slotXnameCheck in userXnames.values():
        for key, value in xnames.items():
            if value == slotXnameCheck:
                return key
            else:
                for key, value in userXnames.items():
                    if value == slotXnameCheck:
                        return key                    
    else:
        return slotXnameCheck

## sets active tab to determine operations on My Cars or Career slots
def activeTab(*args):
    global activeList
    activeList = mainNotebook.index(mainNotebook.select()) + 1
    
## populates car lists from profile
def myCarsListboxPopulate():
    myCarsSlotsList.clear()
    for i in range(20):
        if openProfilePath:
            myCarsSlots[i][0] = checkSlotXname(myCarsSlots[i][1])
        myCarsSlotsList.append(f"{myCarsSlots[i][0]}")
    myCarsSlotsListVar.set(myCarsSlotsList)

def careerListboxPopulate():
    careerSlotsList.clear()
    for i in range(5):
        if openProfilePath:
            careerSlots[i][0] = checkSlotXname(careerSlots[i][1])
        careerSlotsList.append(f"{careerSlots[i][0]}")
    careerSlotsListVar.set(careerSlotsList)

## sets loaded slot index, also enables or disables UI elements depending of slot
def loadSlots(*args):
    global selectedMyCarsSlot
    global selectedCareerSlot
    careerSlotCount = 0
    if activeList == 1:
        selectedMyCarsSlotInput = myCarsListbox.curselection()
        if len(selectedMyCarsSlotInput)==1:
           selectedMyCarsSlot = int(selectedMyCarsSlotInput[0])
        if myCarsSlots[selectedMyCarsSlot][0] == "(empty)":
            clearMyCarsSlotBtn.state(['disabled'])
            exportMyCarsPsetBtn.state(['disabled'])
            exportMyCarsSlotBtn.state(['disabled'])
            myCarsMoveSlotUpBtn.state(['disabled'])
            myCarsMoveSlotDownBtn.state(['disabled'])
        else:
            clearMyCarsSlotBtn.state(['!disabled'])
            exportMyCarsPsetBtn.state(['!disabled'])
            exportMyCarsSlotBtn.state(['!disabled'])
            myCarsMoveSlotUpBtn.state(['!disabled'])
            myCarsMoveSlotDownBtn.state(['!disabled'])

        if selectedMyCarsSlot == 0 and myCarsSlots[selectedMyCarsSlot][0] != '(empty)':
            myCarsMoveSlotUpBtn.state(['disabled'])
            myCarsMoveSlotDownBtn.state(['!disabled'])
        if selectedMyCarsSlot == 19 and myCarsSlots[selectedMyCarsSlot][0] != '(empty)':
            myCarsMoveSlotUpBtn.state(['!disabled'])
            myCarsMoveSlotDownBtn.state(['disabled'])            
        if selectedMyCarsSlot != 0 and selectedMyCarsSlot != 19 and myCarsSlots[selectedMyCarsSlot][0] != '(empty)':
            myCarsMoveSlotUpBtn.state(['!disabled'])
            myCarsMoveSlotDownBtn.state(['!disabled'])
            
    if activeList == 2:
        selectedCareerSlotInput = careerListbox.curselection()
        if len(selectedCareerSlotInput)==1:
           selectedCareerSlot = int(selectedCareerSlotInput[0])
        for i in range(5):
            if careerSlots[i][2][1069:1070] == b'\x00':
                pass
            else:
                careerSlotCount = careerSlotCount+1
        if careerSlots[selectedCareerSlot][0] == "(empty)":
            clearCareerSlotBtn.state(['disabled'])
            exportCareerPsetBtn.state(['disabled'])
            exportCareerSlotBtn.state(['disabled'])
            careerMoveSlotUpBtn.state(['disabled'])
            careerMoveSlotDownBtn.state(['disabled'])
        else:
            clearCareerSlotBtn.state(['!disabled'])
            exportCareerPsetBtn.state(['!disabled'])
            exportCareerSlotBtn.state(['!disabled'])
        if careerSlotCount == 1:
            clearCareerSlotBtn.state(['disabled'])

        if selectedCareerSlot == 0 and careerSlots[selectedCareerSlot][0] != '(empty)':
            careerMoveSlotUpBtn.state(['disabled'])
            careerMoveSlotDownBtn.state(['disabled'])
            clearCareerSlotBtn.state(['disabled'])
        if selectedCareerSlot == 4 and careerSlots[selectedCareerSlot][0] != '(empty)':
            careerMoveSlotUpBtn.state(['!disabled'])
            careerMoveSlotDownBtn.state(['disabled'])
        if selectedCareerSlot != 0 and selectedCareerSlot != 4 and careerSlots[selectedCareerSlot][0] != '(empty)':
            careerMoveSlotUpBtn.state(['!disabled'])
            careerMoveSlotDownBtn.state(['!disabled'])

## opens profile file, then loads slot data and enables UI elements
def openProfile(*args):
    global dirtyFlag
    global openProfilePath
    global openProfilePathPrev
    if dirtyFlag == 1:
        confirmChanges = messagebox.askyesnocancel("Confirm changes", "You have unsaved changes, do you want to save?")
        if confirmChanges is None:
            return
        elif confirmChanges:
            saveProfile()
    if openProfilePath != "":
        openProfilePathPrev = openProfilePath
    openProfilePath = filedialog.askopenfilename(title="Open your NFSU2 save file")
    if openProfilePath == "":
        openProfilePath = openProfilePathPrev
        return
    with open (openProfilePath, 'rb') as profile:
        profile.seek(1196)
        myCarsSlots.clear
        loadUserXnames()
        saveProfileBtn.state(['!disabled'])
        saveAsProfileBtn.state(['!disabled'])
        myCarsListbox['state'] = tk.NORMAL
        exportMyCarsSlotBtn.state(['!disabled'])
        importMyCarsSlotBtn.state(['!disabled'])
        clearMyCarsSlotBtn.state(['!disabled'])
        myCarsMoveSlotUpBtn.state(['!disabled'])
        myCarsMoveSlotDownBtn.state(['!disabled'])
        exportMyCarsPsetBtn.state(['!disabled'])
        importMyCarsPsetBtn.state(['!disabled'])
        careerListbox['state'] = tk.NORMAL
        exportCareerSlotBtn.state(['!disabled'])
        importCareerSlotBtn.state(['!disabled'])
        clearCareerSlotBtn.state(['!disabled'])
        careerMoveSlotUpBtn.state(['!disabled'])
        careerMoveSlotDownBtn.state(['!disabled'])
        exportCareerPsetBtn.state(['!disabled'])
        importCareerPsetBtn.state(['!disabled'])
        for i in range (20):
            myCarsSlots[i][2] = profile.read(1072)
            myCarsSlots[i][1] = myCarsSlots[i][2][24:28]
            if struct.unpack('B', myCarsSlots[i][2][8:9])[0] == 1:
                myCarsSlots[i][0] = checkSlotXname(myCarsSlots[i][1])
            else:
                myCarsSlots[i][0] = '(empty)'
        for i in range (5):
            careerSlots[i][2] = profile.read(1072)
            careerSlots[i][3] = profile.read(962)
            careerSlots[i][1] = careerSlots[i][2][24:28]
            if struct.unpack('B', careerSlots[i][2][1069:1070])[0] == 1:
                careerSlots[i][0] = checkSlotXname(careerSlots[i][1])
            else:
                careerSlots[i][0] = '(empty)'
        profile.close()
    openFileLabel()
    dirtyFlag = 0        
    myCarsListboxPopulate()
    careerListboxPopulate()

## saves profile file
def saveProfile(*args):
    global dirtyFlag
    if openProfilePath:
        with open (openProfilePath, 'r+b') as profile:
            profile.seek(1196)
            for i in range (20):
                profile.write(myCarsSlots[i][2])
            for i in range (5):
                profile.write(careerSlots[i][2])
                profile.write(careerSlots[i][3])
            profile.seek(50639)
            for i in range(20):
                if myCarsSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                    pass
                else:
                    firstFoundMyCarsID = myCarsSlots[i][2][0:4]
                    profile.write(firstFoundMyCarsID)
                    break
            if firstFoundMyCarsID == 0:
                profile.write(struct.pack('>I', b'\x16\x1e\x9b\x95'))
            profile.seek(44415)
            for i in range(5):
                if careerSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                    pass
                else:
                    firstFoundCareerID = careerSlots[i][2][0:4]
                    profile.write(firstFoundCareerID)
                    break
            profile.close()  
        dirtyFlag = 0
        if len(f'File saved to: {openProfilePath}') < 72:
            filePathStr.set(f'File saved to: {openProfilePath}')
        else:
            longpath1= os.path.splitdrive(openProfilePath)
            longpath2= os.path.split(longpath1[1])
            longpath3= os.path.split(longpath2[0])
            longpath4= os.path.split(longpath3[0])
            filePathStr.set(f'File saved to: {longpath1[0]}\\...\\{longpath4[1]}\\{longpath3[1]}\\{longpath2[1]}')
        fileLabel.after(5000, openFileLabel)

## saves profile file as another files
def saveProfileAs(*args):
    global dirtyFlag
    global openProfilePath
    global openProfilePathPrev
    openProfilePathPrev = openProfilePath
    if openProfilePath:
        with open (openProfilePath, 'rb') as profile:
            openProfilePath = profile.read()
            profile.seek(0)
            saveProfilePath = filedialog.asksaveasfilename(title="Save NFSU2 profile as...", filetypes=[("NFSU2 profile", "*.*")])
            if saveProfilePath == "":
                openProfilePath = openProfilePathPrev
                return
            with open (saveProfilePath, 'wb') as profileWrite:
                profileWrite.write(openProfilePath)
                profileWrite.seek(1196)
                for i in range (20):
                    profileWrite.write(myCarsSlots[i][2])
                for i in range (5):
                    profileWrite.write(careerSlots[i][2])
                    profileWrite.write(careerSlots[i][3])
                profileWrite.seek(50639)
                for i in range(20):
                    if myCarsSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                        pass
                    else:
                        firstFoundMyCarsID = myCarsSlots[i][2][0:4]
                        profileWrite.write(firstFoundMyCarsID)
                        break
                if firstFoundMyCarsID == 0:
                    profileWrite.write(struct.pack('>I', b'\x16\x1e\x9b\x95'))
                profileWrite.seek(44415)
                for i in range(5):
                    if careerSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                        pass
                    else:
                        firstFoundCareerID = careerSlots[i][2][0:4]
                        profileWrite.write(firstFoundCareerID)
                profileWrite.close()
            dirtyFlag = 0
            if len(f'File saved to: {saveProfilePath}') < 72:
                filePathStr.set(f'File saved to: {saveProfilePath}')
            else:
                longpath1= os.path.splitdrive(saveProfilePath)
                longpath2= os.path.split(longpath1[1])
                longpath3= os.path.split(longpath2[0])
                longpath4= os.path.split(longpath3[0])
                filePathStr.set(f'File saved to: {longpath1[0]}\\...\\{longpath4[1]}\\{longpath3[1]}\\{longpath2[1]}')
            fileLabel.after(5000, openFileLabel)

## exports selected slot to a .u2cc file, if it's a career mode slot it will also export part inventory data to a .u2ci file
def exportSlot(*args):
    global myCarsSlots
    global careerSlots
    if openProfilePath:
        slotSave = filedialog.asksaveasfilename(title="Export car slot", filetypes=[("MemphisRider custom car slot", "*.u2cc")], defaultextension=[".u2cc"])
        if slotSave == "":
            return
        
        if activeList == 1:
            exportSlots = myCarsSlots
            selSlot = selectedMyCarsSlot
        if activeList == 2:
            exportSlots = careerSlots
            selSlot = selectedCareerSlot
        
        with open (slotSave, 'wb') as slotSaveWrite:
            slotSaveWrite.write(exportSlots[selSlot][2])
            slotSaveWrite.close()
        if activeList == 2:
            slotSaveInv = slotSave.replace(".u2cc", ".u2ci")
            with open (slotSaveInv, 'wb') as slotSaveInvWrite:
                slotSaveInvWrite.write(exportSlots[selSlot][3])
            slotSaveInvWrite.close()
        if len(f'Slot {selSlot+1} exported to: {slotSave}') < 64:
            filePathStr.set(f'Slot {selSlot+1} exported to: {slotSave}')
        else:
            longpath1= os.path.splitdrive(slotSave)
            longpath2= os.path.split(longpath1[1])
            longpath3= os.path.split(longpath2[0])
            longpath4= os.path.split(longpath3[0])
            filePathStr.set(f'Slot {selSlot+1} exported to: {longpath1[0]}\\...\\{longpath3[1]}\\{longpath2[1]}')
        fileLabel.after(5000, openFileLabel)

## imports car in .u2cc file to selected slot, if it's a career mode slot it will also attempt to import part inventory in .u2ci file;
## if not found it will notify user it will use the part inventory from the slot
def importSlot(*args):
    global dirtyFlag
    global myCarsSlots
    global careerSlots

    if openProfilePath:
        slotOpen = filedialog.askopenfilename(title="Import slot to My Cars", filetypes=[("MemphisRider custom car slot", "*.u2cc")])
        if slotOpen == "":
            return
        
        if activeList == 1:
            importSlots = myCarsSlots
            selSlot = selectedMyCarsSlot
        if activeList == 2:
            importSlots = careerSlots
            selSlot = selectedCareerSlot
            
        with open (slotOpen, 'rb') as slotOpenRead:
            importSlots[selSlot][2] = slotOpenRead.read()
            slotOpenRead.close()
            importSlots[selSlot][1] = importSlots[selSlot][2][24:28]
            importSlots[selSlot][0] = checkSlotXname(importSlots[selSlot][1])
            importSlots[selSlot][2] = bytearray(importSlots[selSlot][2])
            if activeList == 1:
                if selSlot < 9:
                    importSlots[selSlot][2][0:4] = f"0{selSlot+1}MC".encode('ascii')
                    importSlots[selSlot][2][4:8] = f"MC0{selSlot+1}".encode('ascii')
                else:
                    importSlots[selSlot][2][0:4] = f"{selSlot+1}MC".encode('ascii')
                    importSlots[selSlot][2][4:8] = f"MC{selSlot+1}".encode('ascii')
                importSlots[selSlot][2][8:9] = struct.pack('>B',1)
                importSlots[selSlot][2][12:13] = struct.pack('>B',2)
            if activeList == 2:
                importSlots[selSlot][2][0:4] = f"0{selSlot+1}CR".encode('ascii')
                importSlots[selSlot][2][4:8] = f"CR0{selSlot+1}".encode('ascii')
                importSlots[selSlot][2][8:9] = struct.pack('>B',1)
                importSlots[selSlot][2][12:13] = struct.pack('>B',4)
                importSlots[selSlot][2][1069:1070] = struct.pack('>B',1)
                slotOpenInv = slotOpen.replace(".u2cc",".u2ci")
                if os.path.isfile(slotOpenInv) == True:
                    with open (slotOpenInv, 'rb') as slotOpenInvRead:
                        importSlots[selSlot][3] = slotOpenInvRead.read()
                        slotOpenInvRead.close()
                else:
                    tk.messagebox.showinfo(title="Attention", message="No part inventory file (*.u2ci) found for this slot. \nImported slot will inherit the inventory from the save file slot.")     
        importSlots[selSlot][2] = bytes(importSlots[selSlot][2])    
        myCarsListboxPopulate()
        careerListboxPopulate()
        loadSlots()
        
        if len(f'Imported {slotOpen} to slot {selSlot+1}') < 72:
            filePathStr.set(f'Imported {slotOpen} to slot {selSlot+1}')
        else:
            longpath1= os.path.splitdrive(slotOpen)
            longpath2= os.path.split(longpath1[1])
            longpath3= os.path.split(longpath2[0])
            longpath4= os.path.split(longpath3[0])
            filePathStr.set(f'Imported {longpath1[0]}\\...\\{longpath3[1]}\\{longpath2[1]} to slot {selSlot+1}')
        fileLabel.after(5000, openFileLabel)
        dirtyFlag = 1

## clears slot data, setting up default data to make slot usable again
def clearSlot(*args):
    global dirtyFlag
    if openProfilePath:
        if activeList == 1:
            carSlots = myCarsSlots
            selSlot = selectedMyCarsSlot
        if activeList == 2:
            carSlots = careerSlots
            selSlot = selectedCareerSlot
        
        carSlots[selSlot][2] = bytearray(b'\x00'*1072)
        carSlots[selSlot][2][8:9] = struct.pack('>B',1)
        carSlots[selSlot][2][856:1061] = bytearray(b'\x64'*205)
        carSlots[selSlot][1] = carSlots[selSlot][2][24:28]
        carSlots[selSlot][0] = '(empty)'
        if activeList == 1:
            carSlots[selSlot][2][12:13] = struct.pack('>B',2)
        if activeList == 2:
            carSlots[selSlot][2][12:13] = struct.pack('>B',4)    
        carSlots[selSlot][2] = bytes(carSlots[selSlot][2])    
        myCarsListboxPopulate()
        careerListboxPopulate()
        loadSlots()
        dirtyFlag = 1

## moves slot up
def moveSlotUp(*args):
    global myCarsSlots
    global careerSlots
    global dirtyFlag
    if openProfilePath:
        if activeList == 1:
            carSlots = myCarsSlots
            selSlot = selectedMyCarsSlot
        if activeList == 2:
            carSlots = careerSlots
            selSlot = selectedCareerSlot

        if selSlot <= 0:
            return
            
        slotMove = carSlots.pop(selSlot)
        slotNewPos = selSlot - 1
        carSlots.insert(slotNewPos, slotMove)
        if activeList == 1:
            for i in range(20):
                if carSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                    i = i+1
                else:
                    carSlots[i][2] = bytearray(carSlots[i][2])
                    if i < 9:
                        carSlots[i][2][0:4] = f"0{i+1}MC".encode('ascii')
                        carSlots[i][2][4:8] = f"MC0{i+1}".encode('ascii')
                    else:
                        carSlots[i][2][0:4] = f"{i+1}MC".encode('ascii')
                        carSlots[i][2][4:8] = f"MC{i+1}".encode('ascii')
                    carSlots[i][2] = bytes(carSlots[i][2])
            myCarsListbox.selection_clear(selSlot)
            myCarsListbox.selection_set(slotNewPos)
        if activeList == 2:
            for i in range(5):
                if carSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                    i = i+1
                else:
                    carSlots[i][2] = bytearray(carSlots[i][2])
                    carSlots[i][2][0:4] = f"0{i+1}CR".encode('ascii')
                    carSlots[i][2][4:8] = f"CR0{i+1}".encode('ascii')
                    carSlots[i][2] = bytes(carSlots[i][2])
            careerListbox.selection_clear(selSlot)
            careerListbox.selection_set(slotNewPos)
        myCarsListboxPopulate()
        careerListboxPopulate()
        loadSlots()
        
        dirtyFlag = 1

## moves slot down
def moveSlotDown(*args):
    global myCarsSlots
    global careerSlots
    global dirtyFlag
    if openProfilePath:
        if activeList == 1:
            carSlots = myCarsSlots
            selSlot = selectedMyCarsSlot
            if selSlot == 19:
                return
        if activeList == 2:
            carSlots = careerSlots
            selSlot = selectedCareerSlot
            if selSlot == 4:
                return
            
        slotMove = carSlots.pop(selSlot)
        slotNewPos = selSlot + 1
        carSlots.insert(slotNewPos, slotMove)
        
        if activeList == 1:
            for i in range(20):
                if carSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                    i = i+1
                else:
                    carSlots[i][2] = bytearray(carSlots[i][2])
                    if i < 9:
                        carSlots[i][2][0:4] = f"0{i+1}MC".encode('ascii')
                        carSlots[i][2][4:8] = f"MC0{i+1}".encode('ascii')
                    else:
                        carSlots[i][2][0:4] = f"{i+1}MC".encode('ascii')
                        carSlots[i][2][4:8] = f"MC{i+1}".encode('ascii')
                    carSlots[i][2] = bytes(carSlots[i][2])
            myCarsListbox.selection_clear(selSlot)
            myCarsListbox.selection_set(slotNewPos)
        if activeList == 2:
            if selSlot == 4:
                return
            for i in range(5):
                if carSlots[i][2][0:4] == b'\x00\x00\x00\x00':
                    i = i+1
                else:
                    carSlots[i][2] = bytearray(carSlots[i][2])
                    carSlots[i][2][0:4] = f"0{i+1}CR".encode('ascii')
                    carSlots[i][2][4:8] = f"CR0{i+1}".encode('ascii')
                    carSlots[i][2] = bytes(carSlots[i][2])
            careerListbox.selection_clear(selSlot)
            careerListbox.selection_set(slotNewPos)
        myCarsListboxPopulate()
        careerListboxPopulate()
        loadSlots()
        
        dirtyFlag = 1

## exports slot data to a Binary-compatible preset file (.bin)
def exportPreset(*args):
    global myCarsSlots
    global careerSlots
    if openProfilePath:
        sponsorFlag = tk.IntVar(value=0)
        spPerfFlag = tk.IntVar(value=0)
        presetName = tk.StringVar(value='')
        
        if activeList == 1:
            exportSlots = myCarsSlots
            selSlot = selectedMyCarsSlot
        if activeList == 2:
            exportSlots = careerSlots
            selSlot = selectedCareerSlot

    ##  dialog to set up parameters like sponsor car flag and performance level
    def exportPresetSettings():
        def exportOkToggle(*args):
            if not presetName.get():
                exportOkBtn.state(['disabled'])
            else:
                exportOkBtn.state(['!disabled'])
                
        def exportOk():
            with open (presetSave, 'wb') as presetWrite:
                presetWrite.write(b'\x00'*76)
                if sponsorFlag.get() != 0:
                    presetWrite.seek(0)
                    presetWrite.write(b'\x40\x14\x43')
                else:
                    pass
                presetWrite.seek(8)
                presetWrite.write(exportSlots[selSlot][0].encode('ascii'))
                presetWrite.seek(40)
                presetWrite.write(presetName.get().upper().encode('ascii'))
                presetWrite.seek(72)
                presetWrite.write(struct.pack('B', spPerfFlag.get()))
                presetWrite.seek(76)
                presetWrite.write(exportSlots[selSlot][2][28:777])
            presetWrite.close()
            exportPresetTop.destroy()
            if len(f'Slot {selSlot+1} exported to: {presetSave}') < 72:
                filePathStr.set(f'Slot {selSlot+1} exported to: {presetSave}')
            else:
                longpath1= os.path.splitdrive(presetSave)
                longpath2= os.path.split(longpath1[1])
                longpath3= os.path.split(longpath2[0])
                longpath4= os.path.split(longpath3[0])
                filePathStr.set(f'Slot {selSlot+1} exported to: {longpath1[0]}\\...\\{longpath3[1]}\\{longpath2[1]}')
            fileLabel.after(5000, openFileLabel)

        def exportCancel():
            exportPresetTop.destroy()
            return
                    
        exportPresetTop = tk.Toplevel(padx='5', pady='5')
        exportPresetTop.title("Export slot as preset")
        exportPresetTop.resizable(False,False)
        if os.name == "nt":
            exportPresetTop.attributes('-toolwindow',1)
        exportPresetTop.grab_set()
        exportPresetNameLbl = ttk.Label(exportPresetTop, text="Enter preset name (up to 32 characters)")
        exportPresetNameLbl.grid(row = 0, column = 0, sticky="W")
        exportPresetNameEnt = ttk.Entry(exportPresetTop, width=50, textvariable=presetName)
        exportPresetNameEnt.grid(row = 1, column = 0, columnspan=2, sticky="WE")
        exportPreIsSponsorChk = ttk.Checkbutton(exportPresetTop, text="Sponsor car", variable=sponsorFlag)
        exportPreIsSponsorChk.grid(row = 2, column = 0, sticky="W")
        exportPreSpPerfLbl = ttk.Label(exportPresetTop, text="Performance level")
        exportPreSpPerfLbl.grid(row = 3, column = 0, sticky="WE")
        exportPreSpPerfLvl0Rd = ttk.Radiobutton(exportPresetTop, text="Stock", variable=spPerfFlag, value=0)
        exportPreSpPerfLvl0Rd.grid(row = 4, column = 0, sticky="WE")
        exportPreSpPerfLvl1Rd = ttk.Radiobutton(exportPresetTop, text="Level 1", variable=spPerfFlag, value=1)
        exportPreSpPerfLvl1Rd.grid(row = 5, column = 0, sticky="WE")
        exportPreSpPerfLvl2Rd = ttk.Radiobutton(exportPresetTop, text="Level 2", variable=spPerfFlag, value=2)
        exportPreSpPerfLvl2Rd.grid(row = 6, column = 0, sticky="WE")
        exportPreSpPerfLvl3Rd = ttk.Radiobutton(exportPresetTop, text="Level 3", variable=spPerfFlag, value=3)
        exportPreSpPerfLvl3Rd.grid(row = 7, column = 0, sticky="WE")
        exportOkBtn = ttk.Button(exportPresetTop, text="OK", command=exportOk, state='disabled')
        exportOkBtn.grid(row = 3, column = 1, sticky="WE")
        exportCancelBtn = ttk.Button(exportPresetTop, text="Cancel", command=exportPresetTop.destroy)
        exportCancelBtn.grid(row = 4, column = 1, sticky="WE")

        exportPresetTop.bind('<KeyRelease>', exportOkToggle)

        regExportP = exportPresetTop.register(inputCallback)
        exportPresetNameEnt.config(validate='key', validatecommand=(regExportP, '%S', '%P')) 

    presetSave = filedialog.asksaveasfilename(title="Export preset", filetypes=[("NFSU2 Binary Preset", "*.bin *.BIN")], defaultextension=[".bin"])
    if presetSave == "":
        return
    if not exportSlots[selSlot][0] in xnames.keys() and not exportSlots[selSlot][0] in userXnames.keys():
        addXnameDlg()
    exportPresetSettings()

## imports preset data from Binary-compatible preset file (.bin)
def importPreset(*args):
    global dirtyFlag
    global newXname
    global newXnameHash
    global myCarsSlots
    global careerSlots
    global presetImportFlag
    
    if openProfilePath:
        if activeList == 1:
            importSlots = myCarsSlots
            selSlot = selectedMyCarsSlot
        if activeList == 2:
            importSlots = careerSlots
            selSlot = selectedCareerSlot
        
        presetOpen = filedialog.askopenfilename(title="Import preset", filetypes=[("NFSU2 Binary Preset", "*.bin *.BIN")])
        if presetOpen == "":
            return
        with open (presetOpen, 'rb') as presetRead:
            presetRead.seek(8)
            presetXname = str(presetRead.read(32)).strip("b'\\x00")
            if not presetXname in xnames.keys() and not presetXname in userXnames.keys():
                newXname.set(presetXname)
                presetImportFlag = 1
                addXnameDlg()
                presetXnameHash = newXnameHash.get()
                if presetXnameHash == '':
                    return
            else:
                if presetXname in xnames.keys():
                    presetXnameHash = xnames[presetXname]
                if presetXname in userXnames.keys():
                    presetXnameHash = userXnames[presetXname]
            presetRead.seek(76)
            presetData = presetRead.read(748)
            presetRead.close()
        newXname.set(presetXnameHash)
        importSlots[selSlot][0] = presetXname
        importSlots[selSlot][1] = struct.pack('>I',int(presetXnameHash,16))
        importSlots[selSlot][2] = bytearray(importSlots[selSlot][2])
        importSlots[selSlot][2][29:776] = presetData
        importSlots[selSlot][2][25:29] = importSlots[selSlot][1]
        if activeList == 1:
            if selSlot < 9:
                importSlots[selSlot][2][0:4] = f"0{selSlot+1}MC".encode('ascii')
                importSlots[selSlot][2][4:9] = f"MC0{selSlot+1}".encode('ascii')
            else:
                importSlots[selSlot][2][0:4] = f"{selSlot+1}MC".encode('ascii')
                importSlots[selSlot][2][4:9] = f"MC{selSlot+1}".encode('ascii')
            importSlots[selSlot][2][8:9] = struct.pack('>B',1)
            importSlots[selSlot][2][12:13] = struct.pack('>B',2)
            importSlots[selSlot][2] = bytes(myCarsSlots[selectedMyCarsSlot][2])
        if activeList == 2:
            if selSlot < 9:
                importSlots[selSlot][2][0:4] = f"0{selSlot+1}CR".encode('ascii')
                importSlots[selSlot][2][4:9] = f"CR0{selSlot+1}".encode('ascii')
            else:
                importSlots[selSlot][2][0:4] = f"{selSlot+1}CR".encode('ascii')
                importSlots[selSlot][2][4:9] = f"CR{selSlot+1}".encode('ascii')
            importSlots[selSlot][2][8:9] = struct.pack('>B',1)
            importSlots[selSlot][2][12:13] = struct.pack('>B',4)
            importSlots[selSlot][2][1069:1070] = struct.pack('>B',1)
            importSlots[selSlot][2] = bytes(importSlots[selSlot][2])
            
        dirtyFlag = 1
        myCarsListboxPopulate()
        careerListboxPopulate()
        loadSlots()
        if len(f'Imported {presetOpen} to slot {selSlot+1}') < 72:
            filePathStr.set(f'Imported {presetOpen} to slot {selSlot+1}')
        else:
            longpath1= os.path.splitdrive(presetOpen)
            longpath2= os.path.split(longpath1[1])
            longpath3= os.path.split(longpath2[0])
            longpath4= os.path.split(longpath3[0])
            filePathStr.set(f'Imported {longpath1[0]}\\...\\{longpath3[1]}\\{longpath2[1]} to slot {selSlot+1}')
        fileLabel.after(5000, openFileLabel)

## opens Add XNAME dialog on button command
def addXnameSolo(*args):
    global activeList
    activeListPrev = activeList
    activeList = 0
    addXnameDlg()
    activeList = activeListPrev
    if openProfilePath:
        myCarsListboxPopulate()
        careerListboxPopulate()

## opens Add XNAME dialog when called, also auto fills XNAME or hash when found
def addXnameDlg():
    global myCarsSlots
    global careerSlots
    global userXnames
    global newXname
    global newXnameHash
    global presetImportFlag
    
    if presetImportFlag == 0:
        newXname.set('')
        newXnameHash.set('')

    if activeList == 1:
        carSlots = myCarsSlots
        selSlot = selectedMyCarsSlot
    if activeList == 2:
        carSlots = careerSlots
        selSlot = selectedCareerSlot

    ## gets hash from a string, thanks to TerminatorVasya for lending me his code
    def hashString(string):
        if string is None:
            return 0
        
        result = -1

        for char in string:
            result = result * 0x21 + ord(char)
        # Mask the result to keep only the last 4 bytes
        result &= 0xFFFFFFFF

        # Convert to bytes in little-endian order (reverse byte order)
        reversed_bytes = result.to_bytes(4, byteorder='big')[::-1]

        # Convert back to hexadecimal string
        return ''.join(f"{byte:02X}" for byte in reversed_bytes)

    ## callback function for XNAME entry field, calls hashString and fills hash entry field on each key release 
    def generateHashString(*args):
        if newXname.get() != '':
            newXnameHashRaw = hashString(newXname.get())
            newXnameHashSet = f"{int(newXnameHashRaw,16):#0{10}x}"
            newXnameHash.set(newXnameHashSet.upper().replace("0X","0x"))
            return newXnameHashSet

    def addXnameOkToggle(*args):
        if not newXname.get():
            addXnameOkBtn.state(['disabled'])
        elif not newXnameHash.get():
            addXnameOkBtn.state(['disabled'])
        else:
            addXnameOkBtn.state(['!disabled'])   
    
    def addXnameOk():
        global presetImportFlag
        with open ("userXnames.txt", 'w') as userXnamesFile:
            newXnameHashWrite = f"{int(newXnameHash.get(),16):#0{10}x}"
            userXnames[newXname.get().upper()] = str(newXnameHashWrite).upper().replace("0X","0x")
            userXnamesFile.write(json.dumps(userXnames, indent=4))
            userXnamesFile.close
        loadUserXnames()
        if openProfilePath:
            carSlots[selSlot][0] = newXname.get().upper()
            myCarsListboxPopulate()
            careerListboxPopulate()
        if presetImportFlag == 0:
            newXname.set('')
            newXnameHash.set('')
        else:
            presetImportFlag = 0
        addXnameTop.destroy()

    def addXnameCancel():
        global presetImportFlag
        newXname.set('')
        newXnameHash.set('')
        presetImportFlag = 0
        addXnameTop.destroy()
        return

    addXnameTop = tk.Toplevel(padx='5', pady='5')
    addXnameTop.title("Add car XNAME and hash")
    addXnameTop.resizable(False,False)
    if os.name == "nt":
        addXnameTop.attributes('-toolwindow',1)
    addXnameTop.minsize(350,150)
    addXnameTop
    addXnameTop.grab_set()
    addXnameMsgLbl = ttk.Label(addXnameTop, text="")
    if activeList == 0:
        addXnameMsgLbl = ttk.Label(addXnameTop, text="Please enter the XNAME and hash to add.\n")
    elif newXname.get() != '' and not newXname.get() in xnames.keys() and not newXname.get() in userXnames.keys() and activeList != 0:
        addXnameMsgLbl = ttk.Label(addXnameTop, text="Car XNAME does not exist in current lists, please add them.\nEnter the XNAME and hash to add.\n")
    elif not carSlots[selSlot][0] in xnames.keys() and not carSlots[selSlot][0] in userXnames.keys() and activeList != 0:
        addXnameMsgLbl = ttk.Label(addXnameTop, text="Car XNAME does not exist in current lists, please add them.\nEnter the XNAME and hash to add.\n")
        newXnameHash.set(carSlots[selSlot][0])
    addXnameMsgLbl.grid(row=0, column=0, columnspan=3, sticky='NSEW')
    addXnameLabel = ttk.Label(addXnameTop, text="XNAME")
    addXnameLabel.grid(row=1, column=0, columnspan=3, sticky='NSEW')
    addXnameEntry = ttk.Entry(addXnameTop, textvariable=newXname)
    addXnameEntry.grid(row=2, column=0, columnspan=3, sticky='NSEW', pady='5')
    addXnameHashLbl = ttk.Label(addXnameTop, text="Hash")
    addXnameHashLbl.grid(row=3, column=0, columnspan=3, sticky='NSEW')
    addXnameHashEnt = ttk.Entry(addXnameTop, textvariable=newXnameHash)
    addXnameHashEnt.grid(row=4, column=0, columnspan=3, sticky='NSEW')
    addXnameOkBtn = ttk.Button(addXnameTop, text="OK", command=addXnameOk, state='disabled')
    addXnameOkBtn.grid(row=5, column=1, pady='5', sticky='E')
    addXnameCancBtn = ttk.Button(addXnameTop, text="Cancel", command=addXnameCancel)
    addXnameCancBtn.grid(row=5, column=2, pady='5', sticky='E')

    if presetImportFlag == 1:
        generateHashString()
        addXnameOkToggle()

    addXnameTop.columnconfigure(0, weight=1)

    regAddXname = addXnameTop.register(inputCallback)
    regAddXnameHex = addXnameTop.register(inputCallbackHex)
    addXnameEntry.config(validate='key', validatecommand=(regAddXname, '%S','%P'))
    addXnameHashEnt.config(validate='key', validatecommand=(regAddXnameHex, '%S','%P'))

    addXnameTop.bind('<KeyRelease>', addXnameOkToggle)
    addXnameEntry.bind('<KeyRelease>', generateHashString)
        
    root.wait_window(addXnameTop)

## defines window widgets
openProfileBtn = ttk.Button(topFrame, image=openBtnIcon, text='Open', style='TopButton.TButton', command=openProfile)
openProfileBtn.grid(row = 0, column=0, sticky='W')
openTip = Hovertip(openProfileBtn, 'Open profile (Ctrl+O)')
saveProfileBtn = ttk.Button(topFrame, image=saveBtnIcon, text='Save', state='disabled', command=saveProfile)
saveProfileBtn.grid(row = 0, column=1, sticky='W')
saveTip = Hovertip(saveProfileBtn, 'Save profile (Ctrl+S)')
saveAsProfileBtn = ttk.Button(topFrame, image=saveAsBtnIcon, text='Save As...', state='disabled', command=saveProfileAs)
saveAsProfileBtn.grid(row = 0, column=2, sticky='W')
saveAsTip = Hovertip(saveAsProfileBtn, 'Save profile as... (Ctrl+Shift+S)')
topSpacerLbl = ttk.Label(topFrame, text='')
topSpacerLbl.grid(row = 0, column = 3, sticky = 'NSEW', padx=100)
addXnameBtn = ttk.Button(topFrame, text='Add XNAME', compound='right', image=addXnameBtnIcon, command=addXnameSolo)
addXnameBtn.grid(row = 0, column=4, sticky="E")
addXnameTip = Hovertip(addXnameBtn, 'Add XNAME (Ctrl+A)')
aboutBtn = ttk.Button(topFrame, image=aboutBtnIcon, text='About', command=aboutDlg)
aboutBtn.grid(row = 0, column=5, sticky="E")
aboutTip = Hovertip(aboutBtn, 'About...')

myCarsListbox = tk.Listbox(myCarsTabLeft, listvariable=myCarsSlotsListVar, exportselection=False, state='disabled')
myCarsListbox.grid(row=0, column=0, columnspan=2, rowspan=15, sticky="NSEW")
myCarsListbox.bind('<<ListboxSelect>>', loadSlots)
myCarsLbScroll = ttk.Scrollbar(myCarsTabLeft, orient=tk.VERTICAL, command=myCarsListbox.yview)
myCarsLbScroll.grid(row=0, column=2, sticky="NSEW")
myCarsListbox.configure(yscrollcommand = myCarsLbScroll.set)
exportMyCarsSlotBtn = ttk.Button(myCarsTabRight, text="Export slot", image=slotExportIcon, compound='left', command=exportSlot, state='disabled', style='TabButton.TButton')
exportMyCarsSlotBtn.grid(row=0, column=0, sticky="NSEW")
exportMyCarsTip = Hovertip(exportMyCarsSlotBtn, 'Export slot (Ctrl+E)')
importMyCarsSlotBtn = ttk.Button(myCarsTabRight, text="Import slot", image=slotImportIcon, compound='left', command=importSlot, state='disabled', style='TabButton.TButton')
importMyCarsSlotBtn.grid(row=1, column=0, sticky="NSEW")
importMyCarsSlotTip = Hovertip(importMyCarsSlotBtn, 'Import slot (Ctrl+I)')
clearMyCarsSlotBtn = ttk.Button(myCarsTabRight, text="Clear slot", image=slotClearIcon, compound='left', command=clearSlot, state='disabled', style='TabButton.TButton')
clearMyCarsSlotBtn.grid(row=2, column=0, sticky="NSEW")
clearMyCarsSlotTip = Hovertip(clearMyCarsSlotBtn, 'Clear slot (Ctrl+Delete)')
myCarsSpacerLbl = ttk.Label(myCarsTabRight, text="")
myCarsSpacerLbl.grid(row=3, column=0, sticky="NSEW", pady='5')
myCarsMoveSlotUpBtn = ttk.Button(myCarsTabRight, text="Move slot up", image=moveSlotUpIcon, compound='left', command=moveSlotUp, state='disabled', style='TabButton.TButton')
myCarsMoveSlotUpBtn.grid(row=4, column=0, sticky="NSEW")
myCarsMoveSlotUpTip = Hovertip(myCarsMoveSlotUpBtn, 'Move slot up (Ctrl+Page Up)')
myCarsMoveSlotDownBtn = ttk.Button(myCarsTabRight, text="Move slot down", image=moveSlotDownIcon, compound='left', command=moveSlotDown, state='disabled', style='TabButton.TButton')
myCarsMoveSlotDownBtn.grid(row=5, column=0, sticky="NSEW")
myCarsMoveSlotDownTip = Hovertip(myCarsMoveSlotDownBtn, 'Move slot down (Ctrl+Page Down)')
myCarsSpacerLbl2 = ttk.Label(myCarsTabRight, text="")
myCarsSpacerLbl2.grid(row=6, column=0, sticky="NSEW", pady='5')
exportMyCarsPsetBtn = ttk.Button(myCarsTabRight, text="Export as preset", image=exportPresetIcon, compound='left', command=exportPreset, state='disabled', style='TabButton.TButton')
exportMyCarsPsetBtn.grid(row=7, column=0, sticky="NSEW")
exportMyCarsPsetTip = Hovertip(exportMyCarsPsetBtn, 'Export as preset (Ctrl+Shift+E)')
importMyCarsPsetBtn = ttk.Button(myCarsTabRight, text="Import preset", image=importPresetIcon, compound='left', command=importPreset, state='disabled', style='TabButton.TButton')
importMyCarsPsetBtn.grid(row=8, column=0, sticky="NSEW")
importMyCarsPsetTip = Hovertip(importMyCarsPsetBtn, 'Import preset (Ctrl+Shift+I)')

careerListbox = tk.Listbox(careerTabLeft, listvariable=careerSlotsListVar, exportselection=False, state='disabled')
careerListbox.grid(row=0, column=0, columnspan=2, rowspan=15, sticky="NSEW")
careerListbox.bind('<<ListboxSelect>>', loadSlots)
careerLbScroll = ttk.Scrollbar(careerTabLeft, orient=tk.VERTICAL, command=careerListbox.yview)
careerLbScroll.grid(row=0, column=2, sticky="NSEW")
careerListbox.configure(yscrollcommand = careerLbScroll.set)
exportCareerSlotBtn = ttk.Button(careerTabRight, text="Export slot", image=slotExportIcon, compound='left', command=exportSlot, state='disabled', style='TabButton.TButton')
exportCareerSlotBtn.grid(row=0, column=0, sticky="NSEW")
exportCareerSlotTip = Hovertip(exportCareerSlotBtn, 'Export slot (Ctrl+E)')
importCareerSlotBtn = ttk.Button(careerTabRight, text="Import slot", image=slotImportIcon, compound='left', command=importSlot, state='disabled', style='TabButton.TButton')
importCareerSlotBtn.grid(row=1, column=0, sticky="NSEW")
importCareerSlotTip = Hovertip(importCareerSlotBtn, 'Import slot (Ctrl+I)')
clearCareerSlotBtn = ttk.Button(careerTabRight, text="Clear slot", image=slotClearIcon, compound='left', command=clearSlot, state='disabled', style='TabButton.TButton')
clearCareerSlotBtn.grid(row=2, column=0, sticky="NSEW")
clearCareerSlotTip = Hovertip(clearCareerSlotBtn, 'Clear slot (Ctrl+Delete)')
careerSpacerLbl = ttk.Label(careerTabRight, text="")
careerSpacerLbl.grid(row=3, column=0, sticky="NSEW", pady='5')
careerMoveSlotUpBtn = ttk.Button(careerTabRight, text="Move slot up", image=moveSlotUpIcon, compound='left', command=moveSlotUp, state='disabled', style='TabButton.TButton')
careerMoveSlotUpBtn.grid(row=4, column=0, sticky="NSEW")
careerMoveSlotUpTip = Hovertip(careerMoveSlotUpBtn, 'Move slot up (Ctrl+Page Up)')
careerMoveSlotDownBtn = ttk.Button(careerTabRight, text="Move slot down", image=moveSlotDownIcon, compound='left', command=moveSlotDown, state='disabled', style='TabButton.TButton')
careerMoveSlotDownBtn.grid(row=5, column=0, sticky="NSEW")
careerMoveSlotDownTip = Hovertip(careerMoveSlotDownBtn, 'Move slot down (Ctrl+Page Down)')
careerSpacerLbl2 = ttk.Label(careerTabRight, text="")
careerSpacerLbl2.grid(row=6, column=0, sticky="NSEW", pady='5')
exportCareerPsetBtn = ttk.Button(careerTabRight, text="Export as preset", image=exportPresetIcon, compound='left', command=exportPreset, state='disabled', style='TabButton.TButton')
exportCareerPsetBtn.grid(row=7, column=0, sticky="NSEW")
exportCareerPsetTip = Hovertip(exportCareerPsetBtn, 'Export as preset (Ctrl+Shift+E)')
importCareerPsetBtn = ttk.Button(careerTabRight, text="Import preset", image=importPresetIcon, compound='left', command=importPreset, state='disabled', style='TabButton.TButton')
importCareerPsetBtn.grid(row=8, column=0, sticky="NSEW")
importCareerPsetTip = Hovertip(importCareerPsetBtn, 'Import preset (Ctrl+Shift+I)')

footSeparator = ttk.Separator(bottomFrame, orient="horizontal")
footSeparator.grid(row = 0, column = 0, sticky="EW")
fileLabel = ttk.Label(bottomFrame, textvariable=filePathStr, width = 10)
fileLabel.grid(row = 1, column = 0, padx=2, pady=2, sticky='EW')

## sets active tab on tab change
mainNotebook.bind("<<NotebookTabChanged>>", activeTab)

## sets key bindings
root.bind('<Control-o>', openProfile)
root.bind('<Control-O>', openProfile)
root.bind('<Control-s>', saveProfile)
root.bind('<Control-S>', saveProfile)
root.bind('<Control-Shift-s>', saveProfileAs)
root.bind('<Control-Shift-S>', saveProfileAs)
root.bind('<Control-a>', addXnameSolo)
root.bind('<Control-A>', addXnameSolo)
root.bind('<Control-e>', exportSlot)
root.bind('<Control-E>', exportSlot)
root.bind('<Control-i>', importSlot)
root.bind('<Control-I>', importSlot)
root.bind('<Control-Delete>', clearSlot)
root.bind('<Control-Prior>', moveSlotUp)
root.bind('<Control-Next>', moveSlotDown)
root.bind('<Control-Shift-e>', exportPreset)
root.bind('<Control-Shift-E>', exportPreset)
root.bind('<Control-Shift-i>', importPreset)
root.bind('<Control-Shift-I>', importPreset)

root.mainloop()
