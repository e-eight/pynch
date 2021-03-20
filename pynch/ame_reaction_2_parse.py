"""Extract the date from the second reaction file."""
import pandas as pd

from pynch.ame_reaction_2_file import AMEReactionFileTwo


class AMEReactionParserTwo(AMEReactionFileTwo):
    """Parse the second AME reaction file.

    The format is known but I don't think python can easily parse it.
    """

    def __init__(self, filename: str, year: int):
        """Set the file to read and table year."""
        super().__init__()
        self.filename = filename
        self.year = year
        print(f"Reading {self.filename} from {self.year}")

    def _read_line(self, line: str) -> dict:
        """Read a line from the file."""
        # Don't use a '#' as an experimental marker in this file
        # but still need to remove it
        if line.find("#") != -1:
            line = line.replace("#", " ")

        data = {"TableYear": self.year}
        data["A"] = self._read_as_int(line, self.START_R2_A, self.END_R2_A)
        data["Z"] = self._read_as_int(line, self.START_R2_Z, self.END_R2_Z)
        data["N"] = data["A"] - data["Z"]
        data["Symbol"] = self.z_to_symbol[data["Z"]]

        data["OneNeutronSeparationEnergy"] = self._read_as_float(line, self.START_SN, self.END_SN)
        data["OneNeutronSeparationEnergyError"] = self._read_as_float(line, self.START_DSN, self.END_DSN)

        data["OneProtonSeparationEnergy"] = self._read_as_float(line, self.START_SP, self.END_SP)
        data["OneProtonSeparationEnergyError"] = self._read_as_float(line, self.START_DSP, self.END_DSP)

        data["QFourBeta"] = self._read_as_float(line, self.START_Q4B, self.END_Q4B)
        data["QFourBetaError"] = self._read_as_float(line, self.START_DQ4B, self.END_DQ4B)

        data["QDeuteronAlpha"] = self._read_as_float(line, self.START_QDA, self.END_QDA)
        data["QDeuteronAlphaError"] = self._read_as_float(line, self.START_DQDA, self.END_DQDA)

        data["QProtonAlpha"] = self._read_as_float(line, self.START_QPA, self.END_QPA)
        data["QProtonAlphaError"] = self._read_as_float(line, self.START_DQPA, self.END_DQPA)

        data["QNeutronAlpha"] = self._read_as_float(line, self.START_QNA, self.END_QNA)
        data["QNeutronAlphaErrror"] = self._read_as_float(line, self.START_DQNA, self.END_DQNA)

        return data

    def read_file(self) -> pd.DataFrame:
        """Read the file."""
        with open(self.filename, "r") as f:
            lines = [line.rstrip() for line in f]

        # Remove the header lines
        lines = lines[self.AME_HEADER:]

        return pd.DataFrame.from_dict([self._read_line(line) for line in lines])
