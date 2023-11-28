import asta

path = 'id_allele1_allele2_probability'

asta.full_algorithm(file_path=path,
                    cutoff_value=2.0,
                    should_save_csv=True,
                    should_save_plot=True)