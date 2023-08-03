import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import PipelineOptions

def remove_is_open(record):
    # Esta función elimina la columna "is_open" del registro
    record.pop("is_open", None)
    return record

def run_pipeline(input_file, output_file):
    # Crea opciones del pipeline para Dataflow
    pipeline_options = PipelineOptions([
        "--runner=DataflowRunner",
        "--project=yelp-394623",
        "--region=us-central1",
        "--temp_location=gs://proyecto-yelp/tmp",  # Cambia YOUR_BUCKET_NAME por el nombre de tu Bucket
    ])

    # Crea el pipeline de Dataflow
    with beam.Pipeline(options=pipeline_options) as pipeline:
        # Lee los datos del archivo .csv
        lines = pipeline | "ReadFromGCS" >> ReadFromText(input_file)

        # Aplica la transformación para eliminar la columna "is_open"
        cleaned_data = lines | "RemoveIsOpenColumn" >> beam.Map(remove_is_open)

        # Escribe los datos limpios en otro archivo .csv
        cleaned_data | "WriteToGCS" >> WriteToText(output_file)

if __name__ == "__main__":
    input_file = "gs://proyecto-yelp/sets/business.csv"    # Cambia YOUR_BUCKET_NAME por el nombre de tu Bucket
    output_file = "gs://proyecto-yelp/sets/output.csv"  # Cambia YOUR_BUCKET_NAME por el nombre de tu Bucket
    run_pipeline(input_file, output_file)
