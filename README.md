# Automated-leaf-disease-segmentation-utilizing-vegtation-indices
A robust implementation of combining vegetation indexes with advanced image processing techniques to segment affected areas of maize leaves

<h3>What are vegetation indexes?</h3>

<p>A vegetation index (VI) is a spectral imaging transformation of two or more image bands designed to enhance the contribution of vegetation properties and allow reliable spatial and temporal inter-comparisons of terrestrial photosynthetic activity and canopy structural variations.</p>

<img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/Readme_img/GeoAwesome.com-Vegetation-Indices-1-Copy.png" width=600px alt="Vegtation index">

The segmentation process is divided into two steps:
<li>Identifying chlorophyll rich areas using vegetation indexes</li>
<li>Removing background using kmeans Filtering</li>

<H3>Extracting healthy green section using VARI Index</H3>

<p>Here instead of using multispectral images we would be using RGB images for the following reasons:</p>
<li>RGB cameras are lot more economical</li>
<li>Spectral images require higher resolution hence more storage space</li>
<li>Easier image processing application</li>
<br>
<table>
  <tr>
    <td><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/Extracted%20images/Original4.jpg" alt="Original" width=400px>
      <p align="center"><b>Original</p>
    </td>
    <td><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/output%20images/EXG%20colormap/Blight%204_colormap.jpg" alt="Excess-Green" width=400px>
      <p align="center"><b>Excess Green Index</p>
    </td>
    <td><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/output%20images/GLI%20colormap/Blight%204_colormap.jpg" alt="Green Leaf index" width=400px>
      <p align="center"><b>Green Leaf Index</p>
    </td>
    <td><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/output%20images/VARI%20colormap/Blight%204_colormap.jpg" alt="Vari" width=400px>
      <p align="center"><b>VARI Index</p>
    </td>
    <td><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/output%20images/VI%20colormap/Blight%204_colormap.jpg" alt="VI index" width=400px>
      <p align="center"><b>VI Index</p>
    </td>
  </tr>
</table>

<p>In the segmentation process however we would mainly be using the VARI Index</p>
<p align="center"><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/Readme_img/d82977b91e4c36028bded9c58ce6f4c4db8ac6af_vari-index-formula.jpg" alt="VARI Index Formula" width=400px></p>

Steps Involved:
<li>Applying VARI on original image</li>
<li>Binarizing the processed image</li>
<li>Inverting pixel values to generate primary disease mask</li>
<li>Primary segmentation</li>
<br>
<p align="center"><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/Readme_img/Screenshot%202023-10-28%20233828.png" alt="Primary segmentation flowchart"></p>
<br>
<p align="center"><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/Readme_img/primary_segmentation.jpg" width=400px></p>
<p align="center"><b>Primary Segmentation</p>
<br>
<H3>Removing background noise using Kmeans Filtering</H3>

Steps Involved:
<li>Implementing K-means on above image with 4 centers</li>
<li>Generating disease mask based on results of k-means</li>
<li>Filtered image</li>
<br>
<p align="center"><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/Readme_img/Kmeans%20segmentation.png"></p>

<br>
<p align="center"><img src="https://github.com/astro189/Automated-maize-disease-segmentation-using-Vegetation-indexes-and-Image-Processing/blob/main/Extracted%20images/EXtraction4.jpg" width=400px></p>
<p align="center">Filtered Image</p>
