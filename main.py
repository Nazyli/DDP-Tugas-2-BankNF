import random, string


def fungsi_file(namafile, operator, data=None):
	with open(namafile, operator) as file:
		if operator == 'a+' or operator == 'w+':
			data = file.writelines(data)
		elif operator == 'r':
			data = file.readlines()
	return data


def bukaRekening(namafile):
	norek = "REK" + ''.join(random.choice(string.digits) for _ in range(3))
	nama = input("Masukkan nama : ")
	saldo = input("Masukkan setoran awal: ")
	fungsi_file(namafile, 'a+', str(norek + ',' + nama + ',' + saldo) + '\n')
	return "Pembukaan rekening dengan nomor " + norek + " atas nama " + nama + " berhasil."


def cekSaldo(namafile, no, nominal, transaksi):
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
					return data, "Saldo tidak mencukupi. Transaksi tunai gagal"
				ls[2] = saldo - nominal
			data[i] = ls[0] + ',' + ls[1] + ',' + str(ls[2]) + '\n'
			break
	if (notFind):
		return data, "Nomor rekening " + no + " tidak terdaftar. Transaksi gagal"
	return data, ""


def editSaldo(namafile, transaksi):
	no = input("Masukkan nomor rekening: ")
	nominal = int(
	    input("Masukkan nominal yang akan di{0}: ".format(transaksi.lower())))
	data, error = cekSaldo(namafile, no, nominal, transaksi)
	if (error != ""):
		return error
	else:
		fungsi_file(namafile, 'w+', data)
		return transaksi + " tunai sebesar " + str(
		    nominal) + " di rekening " + no + " berhasil."


def transfer(namafile):
	noSumber = input("Masukkan nomor rekening sumber: ")
	noTujuan = input("Masukkan nomor rekening tujuan: ")
	nominal = int(input("Masukkan nominal yang akan ditransfer: "))
	data1, error1 = cekSaldo(namafile, noSumber, nominal, "Tarik")
	data2, error2 = cekSaldo(namafile, noTujuan, nominal, "Setor")
	if (error1 != ""):
		return error1
	elif (error2 != ""):
		return error2
	else:
		fungsi_file(namafile, 'w+', data1)
		data2, error2 = cekSaldo(namafile, noTujuan, nominal, "Setor")
		fungsi_file(namafile, 'w+', data2)
		return "Transfer sebesar {0} dari rekening {1} ke rekening {2} berhasil".format(
		    nominal, noSumber, noTujuan)


nasabah = 'nasabah.txt'
isValid = True
pesan = ""
while isValid:
	print(
	    '***** SELAMAT DATANG DI NF BANK *****\nMENU:\n[1] Buka rekening\n[2] Setoran tunai\n[3] Tarik tunai\n[4] Transfer\n[5] Lihat daftar transfer\n[6] Keluar\n'
	)
	menu = input("Masukkan menu pilihan Anda: ")
	print()
	if menu == '1':
		print('*** BUKA REKENING ***')
		pesan = bukaRekening(nasabah)
	elif menu == '2':
		print('*** SETORAN TUNAI ***')
		pesan = editSaldo(nasabah, "Setor")
	elif menu == '3':
		print('*** TARIK TUNAI ***')
		pesan = editSaldo(nasabah, "Tarik")
	elif menu == '4':
		print('*** TRANSFER ***')
		pesan = transfer(nasabah)
	elif menu == '6':
		isValid = False
		pesan = "Terima kasih atas kunjungan Anda..."
	print(pesan + "\n")
