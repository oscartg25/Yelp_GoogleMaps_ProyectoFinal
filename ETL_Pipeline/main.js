const { DataflowPipelineRunner } = require('@apache_beam/runner-dataflow');
const { Pipeline } = require('@apache_beam/pipeline');
const { ReadFromText, WriteToText } = require('@apache_beam/io/textio');

function removeIsOpen(record) {
  // Esta función elimina la columna "is_open" del registro
  delete record['is_open'];
  return record;
}

async function runPipeline(inputFile, outputFile) {
  const pipeline = new Pipeline();

  pipeline.apply(
    ReadFromText(inputFile)
  ).apply(
    'RemoveIsOpenColumn', ParDo.of(removeIsOpen)
  ).apply(
    WriteToText(outputFile)
  );

  const pipelineOptions = {
    runner: DataflowPipelineRunner,
    options: {
      project: 'yelp-394623',
      region: 'us-central1',
      tempLocation: 'gs://proyecto-yelp/tmp',
    },
  };

  await pipeline.run(pipelineOptions);
}

const inputFile = 'gs://proyecto-yelp/sets/business.csv';
const outputFile = 'gs://proyecto-yelp/sets/output.csv';

runPipeline(inputFile, outputFile);
