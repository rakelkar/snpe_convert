# snpe_convert
Scripts to convert and run a TF model using Qualcomm SNPE tools

The tensorflow for poets repo is a good one to get scripts to create and validate a simple PB file and also get training data. This repo has tools that help run SNPE tools on the PB and data....

## Prepare images
Assumes you have created a MobileNet_V1 model from scratch or retrained one using TF for poets walkthrough.

0. Get the data
Based on the TF for poets walkthough
```
curl http://download.tensorflow.org/example_images/flower_photos.tgz \
    | tar xz -C tf_files
    
ls tf_files/flower_photos/ | grep -v LICENSE > labels.txt
```

1. Sample the data
```
random_sample.py tf_files/flower_photos/ samples/
```

2. convert images to raw format (with mean subtraction etc)
```
 python ./toraw.py samples/
 find samples/ -name *.raw > samples.txt
```

## Convert & Quantize
Requires you to have [SNPE tools](https://developer.qualcomm.com/docs/snpe/tools.html) setup

1. convert the model
```
snpe-tensorflow-to-dlc --graph flowers.pb -i input 1,224,224,3 --out_node MobilenetV1/Predictions/Reshape_1 --allow_unconsumed_nodes
```

2. quantize the model
```
snpe-dlc-quantize --input_dlc flowers.dlc --output_dlc flowers_q.dlc --input_list samples.txt
```

## Inference Images
1. run inferencing
```
snpe-net-run --container flowers.dlc --input_list samples.txt --output_dir flower_output

```

2. show results
```
python show_classifications.py -i samples.txt -o flower_output -l labels.txt -s MobilenetV1/Predicti
ons/Reshape_1\: 
```

