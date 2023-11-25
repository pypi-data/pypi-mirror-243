from Orange.data import (ContinuousVariable, Domain, FileFormat, StringVariable, Table, TimeVariable)
import wfdb
import numpy as np
import os

class HDRReader_WFDB(FileFormat):
    """ Reader for WFDB files from PhysioNet.
    It is assumed that there are .dat files with binary data in the same
    directory as the .hea file. For 1001.hea, a file called 1001.dat.
    """
    EXTENSIONS = ('.hea',)
    DESCRIPTION = 'WFDB .hea+.dat files'
    
    def read(self):
        """ Fast reading of spectra. Return spectral information
        in two arrays (wavelengths and values). Only additional
        attributes (usually metas) are returned as a Table.

        Return a triplet:
            - 1D numpy array, (X)
            - 2D numpy array with the same last dimension as xs, (Y)
            - Orange.data.Table with only meta or class attributes
        """
        return HDRReader_WFDB.read_hea(self.filename)
    
    @staticmethod
    def read_hea(filename):
        rec = wfdb.io.rdrecord(filename.replace('.hea', ''))
        rec_name = os.path.basename(filename).replace('.hea', '')

        signal_names = rec.sig_name
        signal_data = rec.p_signal
        signal_length = rec.sig_len
        signal_units = rec.units
        samples_per_second = rec.fs

        timestamps = np.linspace(0, signal_length / samples_per_second, signal_length, endpoint=False)
                
        metas = [
            StringVariable("Record"),
            TimeVariable("Timestamp")
        ]
        for signal_name in signal_names:
            metas.append(ContinuousVariable(signal_name))
            metas.append(StringVariable(signal_name+" units"))
            
        domain = Domain([], None, metas=metas)
        
        metadata = []
        for i, row in enumerate(signal_data):
            rec = [rec_name, timestamps[i]]
            for j, name in enumerate(signal_names):
                rec.append(row[j])
                rec.append(signal_units[j])
            metadata.append(rec)
        
        meta_data = Table.from_numpy(
            domain,
            X=np.zeros((signal_length, 0)),
            metas=np.asarray(metadata, dtype=object)
        )
        
        return meta_data
    
    #read = read_spectra
    
if __name__ == "__main__":
    FileFormat.readers['.hea'] = HDRReader_WFDB
    t = Table("/home/chris/Downloads/ctu-chb-intrapartum-cardiotocography-database-1.0.0/1001.hea")
    print(t)
    