
from tpk.encoder import TPKEncoder

if __name__ == "__main__":
    # Encode texturepacker output files into a TPK file
    # The image format doesn't matter, as long as flash can read it
    encoder = TPKEncoder.from_files("snowninja_idle_anim.png", "snowninja_idle_anim.json")
    encoder.to_file("snowninja_idle_anim.tpk")
