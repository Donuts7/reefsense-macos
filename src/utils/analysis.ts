import { evaluate_segmentation_directory } from './segmentation'

export async function analyzeImages(
  imageFolder: string,
  modelType: string,
  compare: boolean,
  limit?: number
) {
  if (compare) {
    const labelsDir = `${imageFolder}/labels`
    const predictionsDir = `${imageFolder}/predictions`
    
    const metrics = await evaluate_segmentation_directory(
      labelsDir,
      predictionsDir,
      0.5
    )
    
    return formatComparisonResults(metrics)
  }
  
  if (modelType === 'quantify') {
    // Implement quantification logic
    const labelsDir = `${imageFolder}/labels`
    // Process labels and return results
  }
  
  // Regular analysis logic
  return 'Analysis complete'
}

function formatComparisonResults(metrics: any) {
  return `
Segmentation Evaluation Results:
Processed Files: ${metrics.processed_files}
Mean IoU: ${metrics.mean_iou.toFixed(3)}
Precision: ${metrics.precision.toFixed(3)}
Recall: ${metrics.recall.toFixed(3)}
F1 Score: ${metrics.f1_score.toFixed(3)}

Detailed Counts:
True Positives: ${metrics.total_true_positives}
False Positives: ${metrics.total_false_positives}
False Negatives: ${metrics.total_false_negatives}
`
}