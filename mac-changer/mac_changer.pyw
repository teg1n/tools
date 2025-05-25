from tkinter import *
import subprocess
import random
import re
import winreg

root = Tk()
root.title("MAC Address Changer")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#2C3E50")
root.attributes("-topmost", True)
root.wm_attributes("-alpha", 0.9)
root.wm_attributes("-toolwindow", True)

result_label = None

def get_adapters():
    # Ağ adaptörlerinin isimlerini ve registry anahtarlarını döndürür
    adapters = []
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        key = winreg.OpenKey(reg, path)
        for i in range(1000):
            try:
                subkey_name = f"{i:04}"
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    name, _ = winreg.QueryValueEx(subkey, "DriverDesc")
                    netcfg, _ = winreg.QueryValueEx(subkey, "NetCfgInstanceId")
                    adapters.append((name, subkey_name, netcfg))
                except Exception:
                    pass
                subkey.Close()
            except OSError:
                break
        key.Close()
    except Exception:
        pass
    return adapters

def generate_random_mac():
    # İlk baytı çift yap (unicast ve locally administered)
    mac = [random.choice("02468ACE")] + [random.choice("0123456789ABCDEF") for _ in range(11)]
    return "".join(mac)

def change_mac():
    adapter_index = adapter_var.get()
    if not adapter_index:
        result_label.config(text="Lütfen bir adaptör seçin.", fg="red")
        return
    adapters = get_adapters()
    try:
        name, reg_index, netcfg = adapters[int(adapter_index)]
    except Exception:
        result_label.config(text="Geçersiz adaptör.", fg="red")
        return

    new_mac = generate_random_mac()
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + reg_index
        key = winreg.OpenKey(reg, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
        key.Close()
        # Adaptörü devre dışı bırakıp tekrar etkinleştir
        subprocess.call(f'wmic path win32_networkadapter where "GUID=\'{netcfg}\'" call disable', shell=True)
        subprocess.call(f'wmic path win32_networkadapter where "GUID=\'{netcfg}\'" call enable', shell=True)
        result_label.config(
            text=f"Yeni MAC: {':'.join([new_mac[i:i+2] for i in range(0,12,2)])}\nMAC adresi başarıyla değiştirildi!\nBilgisayarı yeniden başlatmanız gerekebilir.",
            fg="green"
        )
    except Exception as e:
        result_label.config(text="MAC adresi değiştirilemedi.\nYönetici olarak çalıştırdığınızdan emin olun.", fg="red")

def reset_mac():
    adapter_index = adapter_var.get()
    if not adapter_index:
        result_label.config(text="Lütfen bir adaptör seçin.", fg="red")
        return
    adapters = get_adapters()
    try:
        name, reg_index, netcfg = adapters[int(adapter_index)]
    except Exception:
        result_label.config(text="Geçersiz adaptör.", fg="red")
        return

    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + reg_index
        key = winreg.OpenKey(reg, path, 0, winreg.KEY_SET_VALUE)
        try:
            winreg.DeleteValue(key, "NetworkAddress")
        except FileNotFoundError:
            pass  # Zaten yoksa sorun değil
        key.Close()
        # Adaptörü devre dışı bırakıp tekrar etkinleştir
        subprocess.call(f'wmic path win32_networkadapter where "GUID=\'{netcfg}\'" call disable', shell=True)
        subprocess.call(f'wmic path win32_networkadapter where "GUID=\'{netcfg}\'" call enable', shell=True)
        result_label.config(
            text="MAC adresi sıfırlandı (fabrika ayarına döndü).\nBilgisayarı yeniden başlatmanız gerekebilir.",
            fg="blue"
        )
    except Exception as e:
        result_label.config(text="MAC adresi sıfırlanamadı.\nYönetici olarak çalıştırdığınızdan emin olun.", fg="red")

adapters = get_adapters()
adapter_var = StringVar()
adapter_names = [f"{i}: {name}" for i, (name, _, _) in enumerate(adapters)]

Label(root, text="Ağ Adaptörü Seçin:", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 11)).pack(pady=(20,0))
adapter_menu = OptionMenu(root, adapter_var, *[str(i) for i in range(len(adapters))])
adapter_menu.config(width=30, font=("Arial", 11), bg="#34495E", fg="#ECF0F1")
adapter_menu.pack(pady=5)

if adapter_names:
    Listbox(root, listvariable=StringVar(value=adapter_names), height=4, width=40, bg="#34495E", fg="#ECF0F1", font=("Arial", 10), selectbackground="#2980B9").pack(pady=2)

Button(root, text="Change MAC Address", command=change_mac, bg="#2980B9", fg="#ECF0F1", font=("Arial", 12), borderwidth=2).pack(pady=10)
Button(root, text="MAC Adresini Sıfırla", command=reset_mac, bg="#27AE60", fg="#ECF0F1", font=("Arial", 12), borderwidth=2).pack(pady=5)

result_label = Label(root, text="", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 11))
result_label.pack(pady=10)

root.mainloop()

