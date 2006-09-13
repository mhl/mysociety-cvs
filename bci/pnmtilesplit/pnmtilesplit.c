/*
 * pnmtilesplit.c:
 * Split a single large PNM file into numerous smaller tiles.
 *
 * Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
 * Email: chris@mysociety.org; WWW: http://www.mysociety.org/
 *
 */

static const char rcsid[] = "$Id: pnmtilesplit.c,v 1.1 2006-09-13 18:40:29 chris Exp $";

#include <sys/types.h>

#include <errno.h>
#include <fcntl.h>
#include <pam.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/wait.h>

#define err(...)    do { fprintf(stderr, "pnmtilesplit: "); fprintf(stderr, __VA_ARGS__); fprintf(stderr, "\n"); } while (0)
#define die(...)    do { err(__VA_ARGS__); exit(1); } while (0)

/* open_output_file FORMAT PIPE I J [PID]
 * Open a new output file, constructing it from FORMAT and the column- and
 * row-index values I and J. If PIPE is non-NULL, open the file via a pipe
 * through the shell. Returns a stdio file handle on success or abort on
 * failure. If PIPE is non-NULL then the process ID of the child process is
 * saved in *PID. */
FILE *open_output_file(const char *fmt, const char *pipe_via,
                        const int i, const int j, pid_t *child_pid) {
    FILE *fp;
    char *filename;
    filename = malloc(strlen(fmt) + 64);
    sprintf(filename, fmt, i, j);
    /* XXX consider creating directories if they don't already exist? */
    if (pipe_via) {
        pid_t p;
        int fd, pp[2];
        if (-1 == (fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644)))
            die("%s: open: %s", filename, strerror(errno));
        else if (-1 == pipe(pp))
            die("pipe: %s", strerror(errno));
        else if (!(fp = fdopen(pp[1], "w")))
            die("fdopen: %s", strerror(errno));
        
        if (-1 == (p = fork()))
            die("fork: %s", strerror(errno));
        else if (0 == p) {
            /* run the pipe command via /bin/sh */
            char *argv[4] = {"/bin/sh", "-c", 0};
            close(0);
            close(1);
            close(pp[1]);
            dup(pp[0]);     /* standard input */
            close(pp[0]);
            dup(fd);        /* standard output */
            close(fd);
            argv[2] = (char*)pipe_via;
            execve("/bin/sh", argv, NULL);
            err("%s: %s", pipe_via, strerror(errno));
            _exit(1);
        } else if (child_pid)
            *child_pid = p;
    } else if (!(fp = fopen(filename, "w")))
        die("%s: open: %s", filename, strerror(errno));

    free(filename);

    return fp;
}

/* usage STREAM
 * Write a usage message to STREAM. */
void usage(FILE *fp) {
    fprintf(fp,
"pnmtilesplit - split a PNM file into fixed-size tiles\n"
"\n"
"Usage: pnmtilesplit -h | [OPTIONS] WIDTH HEIGHT [INPUT]\n"
"\n"
"Split the INPUT image, or, if it is not specified, the image on standard\n"
"input, into WIDTH-by-HEIGHT pixel tiles. If WIDTH or HEIGHT do not divide\n"
"the dimensions of the input image exactly, a warning will be printed and\n"
"the pixels at the extreme right and bottom of the input image will be\n"
"discarded.\n"
"\n"
"Options:\n"
"\n"
"    -h          Display this help message on standard output\n"
"\n"
"    -f FORMAT   Use the printf-style FORMAT for the name of the output file,\n"
"                instead of \"%%d,%%d.pnm\".\n"
"\n"
"    -p COMMAND  Don't write files directly, but pipe them via COMMAND. The\n"
"                COMMAND is interpreted by the shell.\n"
"\n"
"Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.\n"
"Email: chris@mysociety.org; WWW: http://www.mysociety.org/\n"
"%s\n",
            rcsid);
}

/* main ARGC ARGV
 * Entry point. */
int main(int argc, char *argv[]) {
    int tile_w, tile_h, cols, rows;
    char *img_name;
    FILE *img_fp, **tile_fp;
    struct pam img_pam, *tile_pam;
    pid_t *tile_pid;
    char *outfile_format = "%d,%d.pnm", *pipe_via = NULL;
    extern int opterr, optopt, optind;
    static const char optstr[] = "hf:p:";
    int i, j, c;
    tuple *img_row, *tile_row = NULL;

    pnm_init(&argc, argv);
    opterr = 0;

    while (-1 != (c = getopt(argc, argv, optstr))) {
        switch (c) {
            case 'h':
                usage(stdout);
                return 0;

            case 'f':
                outfile_format = optarg;
                break;

            case 'p':
                pipe_via = optarg;
                break;

            case '?':
            default:
                if (strchr(optstr, optopt))
                    err("option -%c requires an argument", optopt);
                else
                    err("unknown option -%c", optopt);
                die("try -h for help");
        }
    }

    if (argc - optind < 2 || argc - optind > 3) {
        err("two or three non-option arguments required");
        die("try -h for help");
    }

    if (0 == (tile_w = atoi(argv[optind])))
        die("\"%s\" is not a valid tile width", argv[optind]);
    else if (0 == (tile_h = atoi(argv[optind + 1])))
        die("\"%s\" is not a valid tile height", argv[optind + 1]);

    if (argv[optind + 2]) {
        img_name = argv[optind + 2];
        if (!(img_fp = fopen(img_name, "rb"))) {
            die("%s: %s", img_name, strerror(errno));
            return 1;
        }
    } else {
        img_name = "(standard input)";
        img_fp = stdin;
    }

    /* lamely, this will just abort if something goes wrong */
    pnm_readpaminit(img_fp, &img_pam, sizeof img_pam);   
    
    /* couple of checks on the image dimensions */
    if (tile_w > img_pam.width)
        die("image width (%d) is smaller than tile width (%d)",
            img_pam.width, tile_w);
    else if (img_pam.width % tile_w) {
        err("warning: tile width does not divide image width exactly");
        err("last %d columns of image will not be included in any tile",
            img_pam.width % tile_w);
    }
    cols = img_pam.width / tile_w;
    
    if (tile_h > img_pam.height)
        die("image height (%d) is smaller than tile height (%d)",
            img_pam.height, tile_h);
    else if (img_pam.height % tile_h) {
        err("warning: tile height does not divide image height exactly");
        err("warning: last %d rows of image will not be included in any tile",
            img_pam.height % tile_h);
    }
    rows = img_pam.height / tile_h;
 
    tile_fp = malloc(cols * sizeof *tile_fp);
    tile_pam = malloc(cols * sizeof *tile_pam);
    tile_pid = malloc(cols * sizeof *tile_pid);
 
    if (!(img_row = pnm_allocpamrow(&img_pam)))
        die("unable to allocate storage for input row");
    
    for (j = 0; j < rows; ++j) {
        int y;

        /* Create output files. */
        for (i = 0; i < cols; ++i) {
            tile_pam[i] = img_pam;
            tile_pam[i].file = tile_fp[i]
                = open_output_file(outfile_format, pipe_via, i, j,
                                    tile_pid + i);
            tile_pam[i].width = tile_w;
            tile_pam[i].height = tile_h;
            pnm_writepaminit(tile_pam + i);

            if (!tile_row && !(tile_row = pnm_allocpamrow(tile_pam + i)))
                die("unable to allocate storage for output row");
        }

        /* Copy the image into the various tiles. */
        for (y = 0; y < tile_h; ++y) {
            int x;
            pnm_readpamrow(&img_pam, img_row);
            for (i = 0; i < cols; ++i) {
                for (x = 0; x < tile_w; ++x)
                    tile_row[x] = img_row[x + i * tile_w];
                pnm_writepamrow(tile_pam + i, tile_row);
                fflush(tile_fp[i]);
            }
        }

        /* Close the output files and check status. */
        for (i = 0; i < cols; ++i) {
            if (-1 == fclose(tile_fp[i]))
                die("while writing tile (%d, %d): %s", i, j, strerror(errno));
            if (pipe_via) {
                /* Collect exit status of child process. */
                pid_t p;
                int st;
                if (-1 == (p = waitpid(tile_pid[i], &st, 0)))
                    die("waitpid: %s", strerror(errno));
                else if (st) {
                    if (WIFEXITED(st))
                        die("child process for tile (%d, %d) failed with "
                            "status %d", i, j, WEXITSTATUS(st));
                    else
                        die("child process for tile (%d, %d) killed by "
                            "signal %d", i, j, WTERMSIG(st));
                }
            }
        }
    }
    return 0;
}
