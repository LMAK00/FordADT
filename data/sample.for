      SUBROUTINE FIBONACCI(*)
      IMPLICIT NONE
C
C FIBONACCI SEQUENCE ALGORITHM
C CREATES A SERIES SUCH THAT EACH NUMBER
C IS A SUM OF THE PREVIOUS
C TWO NUMBERS:
C F0 = 0, F1 = 1
C FN = F(N-1) + F(N-2)
C
      INTEGER N, M
      INTEGER FIB1, FIB2, FIBN
C
C INITIALIZATION
C
      N = 10
      FIB1 = 0
      FIB2 = FIB1
C
      DO 100 M = 0, N
          IF(M .EQ. 0)THEN
              FIB2 = FIB1 + 1
              WRITE(*,*) 'F1 =', FIB1
              WRITE(*,*) 'F2 =', FIB2
          ENDIF
          FIBN = FIB1 + FIB2
          WRITE(*,*) 'FN =', FIB2
          FIB1 = FIB2
          FIB2= FIBN
100   CONTINUE
      END