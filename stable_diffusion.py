import pathlib
import sqlite3
import subprocess
import time

SD_PYTHON = "/home/aymanns/anaconda3/envs/ldm/bin/python"
SD_CONFIG = "/home/aymanns/stable-diffusion/configs/stable-diffusion/v1-inference.yaml"
SD_CKPT = "/home/aymanns/stable-diffusion/models/ldm/stable-diffusion-v1/model.ckpt"
IMG2IMG = "/home/aymanns/stable-diffusion/scripts/img2img.py"
MEDIA_DIR = pathlib.Path(
    "/home/aymanns/projects/Art_Dorota_Egle/stable_diffusion_website/media"
)
JOB_TABLE = "catalog_job"
INPUT_TABLE = "catalog_imginput"
OUTPUT_TABLE = "catalog_imgoutput"


def laod_most_recent(directory):
    pass


def run(img, prompt, strength, seed=42):
    img = MEDIA_DIR / img
    command = [
        SD_PYTHON,
        IMG2IMG,
        "--prompt",
        f"'{prompt}'",
        "--init-img",
        img,
        "--strength",
        f"0.{strength}",
        "--n_samples",
        "1",
        "--seed",
        str(seed),
        "--outdir",
        MEDIA_DIR / "output",
        "--config",
        SD_CONFIG,
        "--ckpt",
        SD_CKPT,
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(error)
    quit()

    if len(error) == 0:
        img = load_most_recent(TMP_DIR)
        return "output/TEST3.jpg"
    else:
        print(error)
        quit()
        return None


if __name__ == "__main__":

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cur.fetchall())
    # print()
    # print("#############")
    # print()

    # cur.execute(f"PRAGMA table_info({JOB_TABLE})")
    # print(cur.fetchall())
    # print()
    # print("#############")
    # print()

    # cur.execute(f"PRAGMA table_info({INPUT_TABLE})")
    # print(cur.fetchall())
    # print()
    # print("#############")
    # print()

    # cur.execute(f"PRAGMA table_info({OUTPUT_TABLE})")
    # print(cur.fetchall())
    # print()
    # print("#############")
    # print()

    cur.execute(f"SELECT * FROM {JOB_TABLE} WHERE status='p' ORDER BY time;")
    pending_rows = cur.fetchall()

    while True:
        for row in pending_rows:
            _, time, strength, prompt, status, input_img_id, _ = row

            cur.execute(f"SELECT * from {INPUT_TABLE} WHERE id={input_img_id}")
            _, _, img = cur.fetchone()

            output_image_path = run(img, prompt, strength)

            cur.execute(
                f"INSERT INTO {OUTPUT_TABLE} (image) VALUES ('{output_image_path}')"
            )
            con.commit()

            cur.execute(
                f"SELECT * FROM {OUTPUT_TABLE} WHERE image='{output_image_path}'"
            )
            output_img_id, path = cur.fetchone()

            cur.execute(
                f"UPDATE {JOB_TABLE} SET status = 'd', output_img_id = {output_img_id} WHERE time='{time}'"
            )
            con.commit()
        time.sleep(1)
