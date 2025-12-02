# Draw.io File Format Specification
**Last Updated:** June 2024

There isn't a single, formal ISO-style specification document for `.drawio` files. Instead, the "specification" is defined by the implementation of the underlying open-source library, **mxGraph**.

However, the format is well-understood. A `.drawio` file is essentially an **XML file** that can exist in two states: **compressed** (default) or **uncompressed**.

Here is the technical breakdown of the file structure.

## 1\. The Container Structure (`.drawio`)

The root element is `<mxfile>`. It contains metadata about the editor version and a `<diagram>` tag for every page in your file.

### Compressed (Default)

Most `.drawio` files you save will look like this to save space. The actual graph data is inside the text content of the `<diagram>` tag, looking like a random string of characters.

```xml
<mxfile host="app.diagrams.net" version="21.0.0" type="device">
  <diagram id="unique-id" name="Page-1">
    7Vtbd6I4EP41PrafDl4e87DP7Mze9sye05mPswgIyDQKiLh1/vUrhEsg4tqdu8...
  </diagram>
</mxfile>
```

**The Compression Algorithm:**
To decode the string inside `<diagram>` tags, you must apply the following steps in reverse order:

1.  **URL Decode** (standard URI component decoding)
2.  **Base64 Decode**
3.  **Inflate** (using raw Deflate algorithm, *without* zlib headers)

### Uncompressed

If you decode the data above (or save the file in draw.io with the "Compressed" checkbox unchecked), you get the raw XML, which defines the visual elements.

```xml
<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" ...>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="My Box" style="rounded=0;" vertex="1" parent="1">
      <mxGeometry x="120" y="120" width="80" height="80" as="geometry" />
    </mxCell>
    ...
  </root>
</mxGraphModel>
```

-----

## 2\. The Core XML Schema (`mxGraphModel`)

This is the heart of the "spec." It describes the diagram using a flat list of cells (`mxCell`), not a nested tree of shapes.

  * **`<root>`**: The container for all cells.
  * **`<mxCell>`**: Represents **Nodes (Vertices)** and **Connections (Edges)**.
      * **`id`**: Unique identifier for the cell.
      * **`parent`**: References the `id` of the container cell (usually layer `1` or root `0`).
      * **`value`**: The text label or HTML content of the shape.
      * **`vertex="1"`**: Indicates this is a shape/node.
      * **`edge="1"`**: Indicates this is a connector/line.
      * **`source` / `target`**: (For edges) References the `id` of the start and end nodes.
      * **`style`**: A semicolon-separated string of key-value pairs (CSS-like) defining the look (e.g., `fillColor=#f8cecc;strokeColor=#b85450;`).
  * **`<mxGeometry>`**: Defines the position (`x`, `y`) and size (`width`, `height`) relative to the parent.

## 3\. Embedded Formats

Draw.io also allows you to save diagrams as images (`.png`, `.svg`) while keeping them editable. It achieves this by embedding the XML data mentioned above into the file's metadata chunks:

  * **PNG:** Stores the XML (often URL-encoded) inside a `zTXt` chunk with the keyword `mxGraphModel`.
  * **SVG:** Stores the XML inside a standard embedded metadata tag or custom attribute.

## 4\. Official Resources

While there is no PDF spec, the following resources act as the de facto specification:

  * **mxGraph XML Codec:** The JavaScript code responsible for encoding/decoding the model.
  * **mxGraphModel Documentation:** The API docs for the model structure.
  * **JGraph GitHub:** The library source code provides the definitive list of valid XML attributes.


