Defining HTML elements to be extracted in a YAML file is a great way to make the web scraper or extractor more configurable and maintainable. To achieve this, use a combination of CSS selectors, XPaths, or other attributes in your YAML file to specify which elements to extract.

1. **Selecting HTML Elements:**

   - **CSS Selectors:** Using CSS selectors is one of the most flexible and reliable methods. You can target elements based on their tag names, classes, IDs, attributes, and their position in the DOM. It's widely supported and easy to use.

     Example in YAML:

     ```yaml
     elements:
       - name: title
         selector: h1
       - name: content
         selector: p
       - name: sidebar
         selector: .sidebar
     ```

   - **XPaths:** XPath expressions allow for more precise and complex selections. You can use XPaths in cases where CSS selectors might not be sufficient, like when you need to select elements based on their attributes, relationships, or specific position in the document.

     Example in YAML:

     ```yaml
     elements:
       - name: title
         selector: //h1
       - name: content
         selector: //div[@class="article-content"]/p
     ```

2. **Selecting Elements in a YAML File:**

   You can define the elements to be extracted in your YAML file by creating a list of elements, where each element has a name (for reference) and a selector. The YAML structure could look like the examples provided above.

   Here's a more complete example in YAML:

   ```yaml
   extraction_config:
     website: "https://example.com"
     elements:
       - name: title
         selector: h1
       - name: content
         selector: p
       - name: sidebar
         selector: .sidebar
   ```

   You can then parse this YAML file in your web extractor script to read the element definitions and use them to extract the data from the web page.
