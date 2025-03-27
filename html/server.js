const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

app.use((req, res, next) => {
    if (req.query.scan) {
        const dirPath = path.join(__dirname, req.path);
        const files = fs.readdirSync(dirPath, { withFileTypes: true });
        
        res.json({
            dirs: files.filter(d => d.isDirectory()).map(d => ({
                name: d.name,
                path: path.join(req.path, d.name),
                files: fs.readdirSync(path.join(dirPath, d.name))
            })),
            files: files.filter(d => d.isFile()).map(d => d.name)
        });
    } else {
        next();
    }
});

app.use(express.static(__dirname));

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});