import os.path
import pathlib
import sqlite3
import subprocess
import time

SD_PYTHON = "/home/aymanns/miniconda3/envs/ldm/bin/python"
SD_CONFIG = "/home/aymanns/stable-diffusion/configs/stable-diffusion/v1-inference.yaml"
SD_CKPT = "/home/aymanns/stable-diffusion/models/ldm/stable-diffusion-v1/model.ckpt"
IMG2IMG = "/home/aymanns/stable-diffusion/scripts/img2img.py"
MEDIA_DIR = pathlib.Path("/home/aymanns/stable_diffusion_website/media")
OUTDIR = MEDIA_DIR / "output"
JOB_TABLE = "catalog_job"
INPUT_TABLE = "catalog_imginput"
OUTPUT_TABLE = "catalog_imgoutput"


def get_most_recent(directory):
    all_files = list(directory.glob("*"))
    most_recent_file = max(all_files, key=os.path.getctime)
    return "output/" + most_recent_file.name


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
        OUTDIR,
        "--config",
        SD_CONFIG,
        "--ckpt",
        SD_CKPT,
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = process.communicate()

    if process.returncode == 0:
        img = get_most_recent(OUTDIR)
        return img
    else:
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

    while True:
        cur.execute(
            f"SELECT time, strength, prompt, status, input_img_id FROM {JOB_TABLE} WHERE status='p' ORDER BY time;"
        )
        pending_rows = cur.fetchall()

        for row in pending_rows:
            job_time, strength, prompt, status, input_img_id = row

            cur.execute(f"SELECT image from {INPUT_TABLE} WHERE id={input_img_id}")
            (img,) = cur.fetchone()

            output_image_path = run(img, prompt, strength)

            cur.execute(
                f"INSERT INTO {OUTPUT_TABLE} (image) VALUES ('{output_image_path}')"
            )
            con.commit()

            cur.execute(
                f"SELECT id, image FROM {OUTPUT_TABLE} WHERE image='{output_image_path}'"
            )
            output_img_id, path = cur.fetchone()

            cur.execute(
                f"UPDATE {JOB_TABLE} SET status = 'd', output_img_id = {output_img_id} WHERE time='{job_time}'"
            )
            con.commit()
        time.sleep(1)
