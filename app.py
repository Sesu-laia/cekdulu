import re
from flask import Flask, render_template, request

app = Flask(__name__)

KATA_KUAT = ["slot", "gacor", "maxwin", "rtp", "scatter", "jackpot", "kakek zeus", "kakek merah", "petir merah", "server luar", "server thailand", "server kamboja", "modal receh", "anti rungkad"]
KATA_LEMAH = ["deposit", "wd", "pola", "bongkar", "receh"]
KATA_PENIPUAN = ["kode otp", "kode verifikasi", "minta pulsa", "transfer dulu", "selamat anda", "pemenang undian", "hadiah", "akun anda diblokir", "rekening anda", "segera konfirmasi", "biaya admin", "pinjaman cepat", "tanpa jaminan"]
PEMENDEK_LINK = ["bit.ly", "s.id", "tinyurl.com", "shorturl.at", "cutt.ly", "t.ly"]
AKHIRAN_ANEH = [".xyz", ".top", ".click", ".vip", ".icu"]


@app.route("/")
def beranda():
    return render_template("index.html")


@app.route("/cek", methods=["POST"])
def cek():
    pesan = request.form["pesan"].lower()

    alasan_bahaya = []
    alasan_hati = []

    # --- cek kata judol ---
    ditemukan_kuat = [kata for kata in KATA_KUAT if kata in pesan]
    ditemukan_lemah = [kata for kata in KATA_LEMAH if kata in pesan]

    if ditemukan_kuat:
        alasan_bahaya.append(f"Ada kata promosi judi online: {', '.join(ditemukan_kuat)}")
    if len(ditemukan_lemah) >= 2:
        alasan_bahaya.append(f"Ada beberapa kata yang sering dipakai judi online: {', '.join(ditemukan_lemah)}")
    elif len(ditemukan_lemah) == 1:
        alasan_hati.append(f"Ada kata yang sering dipakai judi online: {ditemukan_lemah[0]}")

    # --- cek kata penipuan ---
    ditemukan_penipuan = [kata for kata in KATA_PENIPUAN if kata in pesan]
    if len(ditemukan_penipuan) >= 2:
        alasan_bahaya.append(f"Ada beberapa kata yang sering dipakai penipu: {', '.join(ditemukan_penipuan)}")
    elif len(ditemukan_penipuan) == 1:
        alasan_hati.append(f"Ada kata yang sering dipakai penipu: {ditemukan_penipuan[0]}")

    # --- cek link ---
    daftar_link = re.findall(r"https?://\S+|www\.\S+", pesan)
    ditemukan_pemendek = [p for p in PEMENDEK_LINK if p in pesan]
    ditemukan_akhiran = [a for a in AKHIRAN_ANEH if a in pesan]

    if ".apk" in pesan:
        alasan_bahaya.append("Ada file .apk. Penipu sering menyamarkan aplikasi pencuri data sebagai undangan, resi paket, atau tagihan.")
    if ditemukan_pemendek:
        alasan_hati.append(f"Ada link yang disingkat ({', '.join(ditemukan_pemendek)}). Alamat aslinya tersembunyi.")
    if ditemukan_akhiran:
        alasan_hati.append(f"Ada alamat web dengan akhiran yang sering dipakai penipu ({', '.join(ditemukan_akhiran)}).")
    if daftar_link and not ditemukan_pemendek and not ditemukan_akhiran:
        alasan_hati.append("Ada link. Pastikan link berasal dari sumber resmi sebelum diklik.")

    # --- tentukan status akhir ---
    if alasan_bahaya:
        status = "bahaya"
        judul = "BAHAYA"
        saran = "Jangan klik link, jangan pasang aplikasi, dan jangan transfer uang. Hapus pesannya."
    elif alasan_hati:
        status = "hati"
        judul = "HATI-HATI"
        saran = "Jangan buru-buru. Tanyakan dulu ke keluarga sebelum membalas atau klik link."
    else:
        status = "aman"
        judul = "AMAN"
        saran = "Tidak ditemukan ciri penipuan. Tetap waspada kalau ada yang minta uang atau kode OTP."

    semua_alasan = alasan_bahaya + alasan_hati

    return render_template("hasil.html", status=status, judul=judul, saran=saran, semua_alasan=semua_alasan)


if __name__ == "__main__":
    app.run(debug=True, port=5001)