import random
import string
from prettytable import PrettyTable
# python -m pip install -U prettytable

def fungsi_file(namafile, operator, data=None):
    with open(namafile, operator) as file:
        if operator == 'a+' or operator == 'w+':
            data = file.writelines(data)
        elif operator == 'r':
            data = file.readlines()
    return data

def inputNum(message):
    while True:
        x = input(message)
        try:
            return int(x)
            break
        except ValueError:
            print("Hanya menerima input berupa angka!")

def randomKey(awalan):
    return awalan + ''.join(random.choice(string.digits) for _ in range(3))

def bukaRekening(namafile):
    norek = randomKey("REK")
    nama = input("Masukkan nama : ")
    saldo = inputNum("Masukkan setoran awal: ")
    data = norek + ',' + nama + ',' + str(saldo) + '\n'
    fungsi_file(namafile, 'a+', data)
    return "Pembukaan rekening dengan nomor " + norek + " atas nama " + nama + " berhasil."

def cekData(namafile, no, nominal=0, transaksi='Setor'):
    notFind = True
    data = fungsi_file(namafile, 'r')
    for i in range(len(data)):
        ls = data[i].split(',')
        if (no == ls[0]):
            notFind = False
            saldo = int(ls[2])
            if (transaksi.lower() == 'setor'):
                ls[2] = saldo + nominal
            else:
                if (nominal > saldo):
                    return data, "Saldo tidak mencukupi. Transaksi gagal"
                ls[2] = saldo - nominal
            data[i] = ls[0] + ',' + ls[1] + ',' + str(ls[2]) + '\n'
            break
    if (notFind):
      return data, "Nomor rekening " + no + " tidak terdaftar. Transaksi gagal"
    else:
      return data, ""

def editSaldo(namafile, transaksi):
    no = input("Masukkan nomor rekening: ").upper()
    nominal = inputNum("Masukkan nominal yang akan di"+transaksi.lower+": ")
    data, error = cekData(namafile, no, nominal, transaksi)
    if (error != ""):
        return error
    else:
        fungsi_file(namafile, 'w+', data)
        return transaksi + " tunai sebesar " + str(nominal) + " di rekening " + no + " berhasil."

def transferProses(nasabah, transfer):
    idTRF = randomKey("TRF")
    noSumber = input("Masukkan nomor rekening sumber: ").upper()
    noTujuan = input("Masukkan nomor rekening tujuan: ").upper()
    nominal = inputNum("Masukkan nominal yang akan ditransfer: ")
    updateSaldoSumber, err = cekData(nasabah, noSumber, nominal, "Tarik")
    if (err != ""):
        return err
    _, err = cekData(nasabah, noTujuan)
    if (err != ""):
        return err
    else:
        fungsi_file(nasabah, 'w+', updateSaldoSumber)
        updateSaldoTujuan, _ = cekData(nasabah, noTujuan, nominal)
        fungsi_file(nasabah, 'w+', updateSaldoTujuan)
        trfData = idTRF+','+noSumber +','+noTujuan+','+str(nominal)+'\n'
        fungsi_file(transfer, 'a+', trfData)
        return "Transfer sebesar {0} dari rekening {1} ke rekening {2} berhasil".format(nominal, noSumber, noTujuan)


def showTransfer(nasabah, transfer):
    no = input("Masukkan nomor rekening sumber transfer: ").upper()
    data, error = cekData(nasabah, no)
    if (error != ""):
        return "Nomor rekening sumber tidak terdaftar. Transfer gagal."
    else:
        data = fungsi_file(transfer, 'r')
        lsTrf = []
        for i in range(len(data)):
            ls = data[i].strip().split(',')
            if(ls[1] == no):
                lsTrf.append(ls)
        if len(lsTrf) == 0:
            return "Tidak ada data yang ditampilkan."
        else:
            print("Daftar transfer dari rekening", no, ":")
            t = PrettyTable(['ID TRF', 'REK SUMBER', 'REK TUJUAN', 'NOMINAL'])
            t.add_rows(lsTrf)
            print(t)
        return ""


nasabah = 'nasabah.txt'
transfer = 'transfer.txt'
pesan = ""
while True:
    print(
        '\n***** SELAMAT DATANG DI NF BANK *****\nMENU:\n[1] Buka rekening\n[2] Setoran tunai\n[3] Tarik tunai\n[4] Transfer\n[5] Lihat daftar transfer\n[6] Keluar\n'
    )
    menu = inputNum("Masukkan menu pilihan Anda: ")
    if menu == 1:
        print('*** BUKA REKENING ***')
        pesan = bukaRekening(nasabah)
    elif menu == 2:
        print('*** SETORAN TUNAI ***')
        pesan = editSaldo(nasabah, "Setor")
    elif menu == 3:
        print('*** TARIK TUNAI ***')
        pesan = editSaldo(nasabah, "Tarik")
    elif menu == 4:
        print('*** TRANSFER ***')
        pesan = transferProses(nasabah, transfer)
    elif menu == 5:
        print('*** LIHAT DATA TRANSFER ***')
        pesan = showTransfer(nasabah, transfer)
    elif menu == 6:
        break
        pesan = "Terima kasih atas kunjungan Anda..."
    else:
        pesan = "Pilihan Anda tidak terdaftar. Ulangi"
    print(pesan + "\n")
