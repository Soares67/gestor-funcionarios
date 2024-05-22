from customtkinter import CTkImage
from PIL import Image
 

img = Image.open(r"Icons\imgs\icons8-home-24.png")
HOME_ICON = CTkImage(light_image=img, size=(32, 31))

img1 = Image.open(r'Icons\imgs\icons8-settings-144.png')
SETTINGS_ICON = CTkImage(light_image=img1, size=(32, 31))

img2 =  Image.open(r'Icons\imgs\icons8-close-250.png')
CLOSE_ICON = CTkImage(light_image=img2, size=(32, 31))

img3 = Image.open(r'Icons\imgs\icons8-admin-90.png')
ADMIN_ICON = CTkImage(light_image=img3, size=(32, 31))

img4 = Image.open(r'Icons\imgs\icons8-eye-90.png')
EYE_ICON = CTkImage(light_image=img4, size=(15, 15))

img5 = Image.open(r'Icons\imgs\icons8-closed-eye-50.png')
CLOSED_EYE_ICON = CTkImage(light_image=img5, size=(15, 15))

img6 = Image.open(r'Icons\imgs\icons8-payroll-64.png')
FOLHA_PAGAMENTO_ICON = CTkImage(light_image=img6, size=(32, 31))

img7 = Image.open(r'Icons\imgs\icons8-calendar-96.png')
FERIAS_ICON = CTkImage(light_image=img7, size=(33, 32))

img8 = Image.open(r'Icons\imgs\icons8-register-100.png')
CADASTRO_ICON = CTkImage(light_image=img8, size=(32, 31))

img9 = Image.open(r'Icons\imgs\icons8-report-64.png')
RELATORIO_ICON = CTkImage(light_image=img9, size=(32, 31))

img10 = Image.open(r'Icons\imgs\icons8-time-is-money-64.png')
HORA_EXTRA_ICON = CTkImage(light_image=img10, size=(32, 31))

img11 = Image.open(r'Icons\imgs\icons8-graphic-64.png')
PROMOVER_ICON = CTkImage(light_image=img11, size=(32, 31))

img12 = Image.open(r'Icons\imgs\icons8-moon-100.png')
MOON_ICON = CTkImage(light_image=img12, size=(32, 31))

img13 = Image.open(r'Icons\imgs\icons8-sun-50.png')
SUN_ICON = CTkImage(light_image=img13, size=(32, 31))

employees_img = Image.open(r'Icons\imgs\employees.png')
EMPLOYEES_IMG = CTkImage(light_image=employees_img, size=(368, 269))

refresh_icon = Image.open(r'Icons\imgs\icons8-refresh-32.png')
REFRESH_ICON = CTkImage(light_image=refresh_icon, size=(32, 31))

promoted_icon = Image.open(r'Icons\imgs\promoted-employee.jpg')
PROMOTED_ICON = CTkImage(light_image=promoted_icon, size=(342, 342))

fired_icon = Image.open(r'Icons\imgs\fired-employee.jpg')
FIRED_ICON = CTkImage(light_image=fired_icon, size=(342, 342))

search_icon = Image.open(r'Icons\imgs\icons8-search-100.png')
SEARCH_ICON = CTkImage(light_image=search_icon, size=(32, 31))