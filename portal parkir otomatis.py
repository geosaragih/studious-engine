#Program portal parkir otomatis
#mendaftarkan plat lalu mendapat kode lalu untuk keluar parkiran harus memasukkan kode dan plat

#KAMUS
#plat,platnomor : string
#jam, menit ,detik, totaldetik, waktu, waktudb, kode : integer
#masukan1, masukan2, masukan3 : entry
#label1, label2, label3, label4, label5, label6 : label
#tombol_1, tombol_2, tombol_3, tombol_4, tombol_5 : button
#windowsbaru, ambil, windowsbaru2, database, selectdb, benar, windowsbaru3, box : function
#db, conn, data, data2, simpan : sqlite3 funcion

#mengimpor modul-modul yang diperlukan
from tkinter import *
from datetime import datetime
import tkinter.messagebox as box
import sqlite3

#ALGORITMA UTAMA
#mengambil waktu saat ini
now=datetime.now()
jam=now.hour#mengambil jam saat ini
menit=now.minute#mengambil menit saat ini
detik=now.second#mengambil detik saat ini
waktu=str(jam**2+menit**3+detik**7)#menjadikan kombinasi dari angka waktu menjadi kode
totaldetik=((jam*3600)+(menit*60)+(detik*1))#menghitung total detik waktu saat ini

#FUNGSI-FUNGSI
#fungsi memanggil windowsbaru
def windowsbaru():
    #syntax memanggil windowbaru
    window = Tk()
    window.title('Selamat Datang')
    window.configure(background='white')

    ##memberi tulisan di dalam windowbaru
    label1 = Label(window, text="Plat Nomor ")
    label1.pack(padx=15, pady=5)
    label1.configure(background='white')

    #membuat kotak input plat nomor
    masukan1 = Entry(window, bd=5)
    masukan1.pack(padx=15, pady=5)

    #fungsi mengambil plat hasil input dari platnomor
    def ambil():
        plat = masukan1.get()#mengambil plat dari input platnomor
        box.showinfo('tiket','plat Nomor = {}  , kode = {}'.format(plat,waktu))#memunculkan notifikasi plat dan kode
        return database(plat)

    #fungsi memasukkan data plat,waktu(kode), dan total detik saat menginput ke database
    def database(plat):
        db = sqlite3.connect("pengendara.db")
        conn = db.cursor()
        simpan = "INSERT INTO datapengendara VALUES('{}', {}, {})".format(plat, waktu, totaldetik)
        conn.execute(simpan)
        db.commit()

    #tombol untuk memanggil fungsi ambil
    tombol_1 = Button(window, text='DAFTARKAN', padx=100, pady=50, command=ambil)
    tombol_1.pack(padx=20, pady=25)

    window.mainloop()

#fungsi memanggil windowsbaru2
def windowsbaru2():
    window = Tk()
    window.title('keluar')
    window.configure(background='white')

    #fungsi mengambil plat dan kode dari database
    def selectdb(pelat, kode):
       db = sqlite3.connect("pengendara.db")
       conn = db.cursor()
       data = conn.execute('SELECT * FROM datapengendara WHERE pelat="{}" and kode={}'.format(pelat, kode))
       data2 = data.fetchone()
       return data2

    #fungsi untuk menghapus data (plat,waktu, dan kode) setelah sepeda motor keluar dan membayar
    def benar():
        platnomor = masukan2.get()
        kode = masukan3.get()

        try:#mencoba menguji adakah kombinasi plat dan kode dalam database
            data = selectdb(platnomor, kode)
            waktudb = data[2]
            db = sqlite3.connect("pengendara.db")
            conn = db.cursor()
            conn.execute("""DELETE FROM datapengendara WHERE kode = {}""".format(kode))
            db.commit()
            conn.close()

            #mengambil waktu saat keluar parkir
            now = datetime.now()
            jam = now.hour
            menit = now.minute
            sekon = now.second
            detik = ((jam * 3600) + (menit * 60) + (sekon * 1))#total detik saat keluar parkiran
            harga = (abs(detik - waktudb)//1800)*1500 #berharga 1500 per setengah jamnya

            #fungsi memanggil windowsbaru3
            def windowsbaru3 ():
                window = Tk()
                window.title('Pembayaran')
                window.configure(background='white')

                #memunculkan harga yang harus dibayar
                label2 = Label(window, text='RP ' + "{}".format(str(harga)))
                label2.pack(padx=15, pady=5)
                label2.configure(background='white')

                #fungsi memanggil notifikasi
                def box():
                     global box
                     box.showinfo('info', 'PORTAL TERBUKA')

                #tombol bayar
                tombol_2 = Button(window, text='BAYAR', padx=100, pady=50, command=box)
                tombol_2.pack(padx=20, pady=25)
            windowsbaru3()

        except:#jika kombinasi plat dan kode ada dalam database
            box.showinfo('info', 'Plat dan Kode tidak valid')

    frame = Frame(window)

    #menuliskan tulisan pada window
    label3 = Label(window, text="Plat Nomor")
    label3.pack(padx=15, pady=5)
    label3.configure(background='white')

    #membuat kotak input Plat Nomor
    masukan2 = Entry(window, bd=5)
    masukan2.pack(padx=15, pady=5)

    #menuliskan tulisan pada window
    label4 = Label(window, text='Kode ')
    label4.pack(padx=15, pady=6)
    label4.configure(background='white')

    #membuat kotak input kode
    masukan3 = Entry(window, bd=5)
    masukan3.pack(padx=15, pady=7)

    #membuat tombol login
    tombol_3 = Button(frame, text='LOGIN', command=benar)
    tombol_3.pack(side=LEFT, padx=0)
    frame.pack(padx=100, pady=19)
    tombol_3.configure(background='white')
    window.mainloop()

#ALGORITMA UTAMA
#memanggil window
window = Tk()
window.title('mendaftarkan pengendara')
window.configure(background='white',padx=430,pady=230)
frame = Frame(window)

#menuliskan tulisan pada window
label5 = Label(window, text='Selamat Datang',font='castellar',padx=15, pady=6)
label5.grid(column=0,rowspan=1,row=2)
label5.configure(background='white')

#menuliskan tulisan pada window
label6 = Label(window, text='Selamat parkir',font='castellar',padx=15, pady=6)
label6.grid(column=1,rowspan=3,row=4)
label6.configure(background='white')

#membuat tombol untuk masuk parkir
tombol_4 = Button(window, text = 'MASUK',command = windowsbaru,padx=100,pady=50)
tombol_4.grid(column=1,rowspan=2,row=2)

#membuat tombol untuk keluar parkir
tombol_5 = Button(window, text = 'KELUAR',command = windowsbaru2,padx=100,pady=50)
tombol_5.grid(column=0,rowspan=3,row=4)

window.mainloop()

















