# Mediasorter (server)

This is a straightforward web interface for the [mediasorter](https://github.com/xyzjonas/mediasorter) utility. Configured folders can be scanned, and detected media files can be selected individually for sorting, eliminating unwanted sorting mistakes compared to a CRON-based setup.

### Install
```bash
 pip install mediasorter-server
```

### Usage
```bash
# CLI tool
mediasorter --help
```

```bash
# use --setup to start with a default configuration file
mediasorter --setup
```

```bash
# start the all-in-one server (valid configuration is needed)
mediasorter-server
```
